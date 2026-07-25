import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, joinedload

from app.models.client import Client
from app.models.proposal import Proposal
from app.models.user import User
from app.schemas.proposal import ProposalCreate, ProposalStatusUpdate, ProposalUpdate

ALLOWED_PROPOSAL_STATUSES = {"Draft", "Sent", "Revised", "Approved", "Rejected"}


def get_client_or_404(db: Session, client_id: uuid.UUID) -> Client:
    client = db.get(Client, client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    return client


def create_proposal(db: Session, payload: ProposalCreate, current_user: User) -> Proposal:
    get_client_or_404(db, payload.client_id)
    proposal = Proposal(
        client_id=payload.client_id,
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
    db.commit()
    db.refresh(proposal)
    return proposal


def build_proposals_query(
    search: str | None = None,
    client_id: uuid.UUID | None = None,
    status_filter: str | None = None,
    research_type: str | None = None,
) -> Select[tuple[Proposal]]:
    statement = select(Proposal).options(joinedload(Proposal.client))
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
        .options(joinedload(Proposal.client))
        .where(Proposal.id == proposal_id)
    )
    return db.execute(statement).scalar_one_or_none()


def update_proposal(db: Session, proposal_id: uuid.UUID, payload: ProposalUpdate) -> Proposal | None:
    proposal = get_proposal_by_id(db, proposal_id)
    if proposal is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if "proposal_title" in update_data and update_data["proposal_title"] is not None:
        update_data["proposal_title"] = update_data["proposal_title"].strip()

    for field, value in update_data.items():
        setattr(proposal, field, value)

    db.commit()
    db.refresh(proposal)
    return proposal


def update_proposal_status(db: Session, proposal_id: uuid.UUID, payload: ProposalStatusUpdate) -> Proposal | None:
    proposal = get_proposal_by_id(db, proposal_id)
    if proposal is None:
        return None

    if payload.status not in ALLOWED_PROPOSAL_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid proposal status",
        )

    proposal.status = payload.status
    proposal.approved_at = datetime.utcnow() if payload.status == "Approved" else None
    db.commit()
    db.refresh(proposal)
    return proposal
