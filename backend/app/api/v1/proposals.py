import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.proposal import Proposal
from app.models.user import User
from app.schemas.proposal import (
    ProposalCreate,
    ProposalDetail,
    ProposalListItem,
    ProposalStatusUpdate,
    ProposalUpdate,
)
from app.services.proposals import (
    create_proposal,
    get_proposal_by_id,
    list_proposals,
    update_proposal,
    update_proposal_status,
)

router = APIRouter(prefix="/proposals", tags=["proposals"])


def to_list_item(proposal: Proposal) -> ProposalListItem:
    return ProposalListItem(
        id=proposal.id,
        proposal_number=proposal.proposal_number,
        client_id=proposal.client_id,
        client_name=proposal.client.client_name,
        proposal_owner=proposal.proposal_owner,
        proposal_title=proposal.proposal_title,
        research_type=proposal.research_type,
        estimated_budget=proposal.estimated_budget,
        status=proposal.status,
        created_at=proposal.created_at,
    )


@router.get("", response_model=list[ProposalListItem])
def get_proposals(
    search: str | None = Query(default=None),
    client_id: uuid.UUID | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    research_type: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ProposalListItem]:
    proposals = list_proposals(
        db,
        search=search,
        client_id=client_id,
        status_filter=status_filter,
        research_type=research_type,
    )
    return [to_list_item(proposal) for proposal in proposals]


@router.post("", response_model=ProposalDetail, status_code=status.HTTP_201_CREATED)
def post_proposal(
    payload: ProposalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProposalDetail:
    return create_proposal(db, payload, current_user)


@router.get("/{proposal_id}", response_model=ProposalDetail)
def get_proposal(
    proposal_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProposalDetail:
    proposal = get_proposal_by_id(db, proposal_id)
    if proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    return proposal


@router.patch("/{proposal_id}", response_model=ProposalDetail)
def patch_proposal(
    proposal_id: uuid.UUID,
    payload: ProposalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProposalDetail:
    proposal = update_proposal(db, proposal_id, payload, current_user)
    if proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    return proposal


@router.patch("/{proposal_id}/status", response_model=ProposalDetail)
def patch_proposal_status(
    proposal_id: uuid.UUID,
    payload: ProposalStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProposalDetail:
    proposal = update_proposal_status(db, proposal_id, payload, current_user)
    if proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    return proposal
