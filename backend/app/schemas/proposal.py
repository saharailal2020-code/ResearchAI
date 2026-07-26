import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProposalCreate(BaseModel):
    client_id: uuid.UUID
    proposal_title: str
    research_type: str | None = None
    research_objective: str | None = None
    methodology_summary: str | None = None
    estimated_timeline: str | None = None
    estimated_budget: Decimal | None = None


class ProposalUpdate(BaseModel):
    proposal_title: str | None = None
    research_type: str | None = None
    research_objective: str | None = None
    methodology_summary: str | None = None
    estimated_timeline: str | None = None
    estimated_budget: Decimal | None = None


class ProposalStatusUpdate(BaseModel):
    status: str


class ProposalOwnerResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ProposalListItem(BaseModel):
    id: uuid.UUID
    proposal_number: str
    client_id: uuid.UUID
    client_name: str
    proposal_owner: ProposalOwnerResponse | None
    proposal_title: str
    research_type: str | None
    estimated_budget: Decimal | None
    status: str
    created_at: datetime


class ProposalDetail(BaseModel):
    id: uuid.UUID
    proposal_number: str
    client_id: uuid.UUID
    proposal_owner: ProposalOwnerResponse | None
    proposal_title: str
    research_type: str | None
    research_objective: str | None
    methodology_summary: str | None
    estimated_timeline: str | None
    estimated_budget: Decimal | None
    status: str
    approved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
