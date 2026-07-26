import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, joinedload

from app.models.client import Client, ClientActivity
from app.models.proposal import Proposal
from app.models.user import User
from app.schemas.proposal import ProposalCreate, ProposalStatusUpdate, ProposalUpdate

ALLOWED_PROPOSAL_STATUSES = {"Draft", "Sent", "Revised", "Approved", "Rejected"}
STATUS_ALIASES = {
    "Sent to Client": "Sent",
    "Revision": "Revised",
}


def get_client_or_404(db: Session, client_id: uuid.UUID) -> Client:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    return client


def generate_proposal_number(db: Session) -> str:
    today_key = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"PROP-{today_key}"
    count_statement = select(func.count()).select_from(Proposal).where(
        Proposal.proposal_number.like(f"{prefix}-%")
    )
    sequence = int(db.execute(count_statement).scalar_one()) + 1

    while True:
        proposal_number = f"{prefix}-{sequence:04d}"
        existing = db.execute(
            select(Proposal.id).where(Proposal.proposal_number == proposal_number)
        ).scalar_one_or_none()
        if existing is None:
            return proposal_number
        sequence += 1


def record_proposal_activity(
    db: Session,
    proposal: Proposal,
    current_user: User,
    activity_title: str,
    activity_description: str,
) -> None:
    now = datetime.utcnow()
    proposal.client.last_activity_at = now
    db.add(
        ClientActivity(
            client_id=proposal.client_id,
            activity_type="Proposal",
            activity_title=activity_title,
            activity_description=activity_description,
            source_type="Proposal",
            source_id=proposal.id,
            activity_at=now,
            created_by=current_user.id,
        )
    )


def create_proposal(db: Session, payload: ProposalCreate, current_user: User) -> Proposal:
    client = get_client_or_404(db, payload.client_id)
    proposal = Proposal(
        proposal_number=generate_proposal_number(db),
        client_id=payload.client_id,
        proposal_owner_id=current_user.id,
        proposal_title=payload.proposal_title.strip(),
        research_type=payload.research_type,
        research_objective=payload.research_objective,
        methodology_summary=payload.methodology_summary,
        estimated_timeline=payload.estimated_timeline,
        estimated_budget=payload.estimated_budget,
        status="Draft",
        created_by=current_user.id,
    )
    db.add(proposal)
    db.flush()
    proposal.client = client
    record_proposal_activity(
        db,
        proposal,
        current_user,
        "Proposal dibuat",
        f"Proposal {proposal.proposal_title} telah dibuat.",
    )
    db.commit()
    db.refresh(proposal)
    return get_proposal_by_id(db, proposal.id)


def build_proposals_query(
    search: str | None = None,
    client_id: uuid.UUID | None = None,
    status_filter: str | None = None,
    research_type: str | None = None,
) -> Select[tuple[Proposal]]:
    statement = select(Proposal).options(joinedload(Proposal.client), joinedload(Proposal.proposal_owner))
    if search:
        statement = statement.where(func.lower(Proposal.proposal_title).contains(search.lower()))
    if client_id:
        statement = statement.where(Proposal.client_id == client_id)
    if status_filter:
        statement = statement.where(Proposal.status == status_filter)
    if research_type:
        statement = statement.where(func.lower(Proposal.research_type).contains(research_type.lower()))
    return statement.order_by(Proposal.created_at.desc())


def list_proposals(
    db: Session,
    search: str | None = None,
    client_id: uuid.UUID | None = None,
    status_filter: str | None = None,
    research_type: str | None = None,
) -> list[Proposal]:
    statement = build_proposals_query(
        search=search,
        client_id=client_id,
        status_filter=status_filter,
        research_type=research_type,
    )
    return list(db.execute(statement).scalars().all())


def get_proposal_by_id(db: Session, proposal_id: uuid.UUID) -> Proposal | None:
    statement = (
        select(Proposal)
        .options(joinedload(Proposal.client), joinedload(Proposal.proposal_owner))
        .where(Proposal.id == proposal_id)
    )
    return db.execute(statement).scalar_one_or_none()


def update_proposal(db: Session, proposal_id: uuid.UUID, payload: ProposalUpdate, current_user: User) -> Proposal | None:
    proposal = get_proposal_by_id(db, proposal_id)
    if proposal is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        return proposal

    if "proposal_title" in update_data and update_data["proposal_title"] is not None:
        update_data["proposal_title"] = update_data["proposal_title"].strip()

    for field, value in update_data.items():
        setattr(proposal, field, value)

    record_proposal_activity(
        db,
        proposal,
        current_user,
        "Proposal diperbarui",
        f"Detail proposal {proposal.proposal_title} telah diperbarui.",
    )
    db.commit()
    db.refresh(proposal)
    return get_proposal_by_id(db, proposal.id)


def normalize_proposal_status(status_value: str) -> str:
    return STATUS_ALIASES.get(status_value, status_value)


def get_status_activity(proposal_title: str, new_status: str) -> tuple[str, str]:
    if new_status == "Sent":
        return "Proposal dikirim ke client", f"Proposal {proposal_title} telah dikirim ke client."
    if new_status == "Revised":
        return "Proposal perlu revisi", f"Proposal {proposal_title} perlu direvisi."
    if new_status == "Approved":
        return "Proposal disetujui", f"Proposal {proposal_title} telah disetujui."
    if new_status == "Rejected":
        return "Proposal ditolak", f"Proposal {proposal_title} telah ditolak."
    return "Status proposal diperbarui", f"Status proposal {proposal_title} diperbarui menjadi {new_status}."


def update_proposal_status(
    db: Session,
    proposal_id: uuid.UUID,
    payload: ProposalStatusUpdate,
    current_user: User,
) -> Proposal | None:
    proposal = get_proposal_by_id(db, proposal_id)
    if proposal is None:
        return None

    new_status = normalize_proposal_status(payload.status)
    if new_status not in ALLOWED_PROPOSAL_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid proposal status",
        )

    if proposal.status == new_status:
        return proposal

    proposal.status = new_status
    proposal.approved_at = datetime.utcnow() if new_status == "Approved" else None
    activity_title, activity_description = get_status_activity(proposal.proposal_title, new_status)
    record_proposal_activity(db, proposal, current_user, activity_title, activity_description)
    db.commit()
    db.refresh(proposal)
    return get_proposal_by_id(db, proposal.id)
