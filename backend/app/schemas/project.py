import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProjectSetupCreate(BaseModel):
    project_name: str


class ProjectStatusUpdate(BaseModel):
    status: str


class ProjectUserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class ProjectClientSummary(BaseModel):
    id: uuid.UUID
    client_name: str
    city: str | None
    industry: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class ProjectProposalSummary(BaseModel):
    id: uuid.UUID
    proposal_number: str
    proposal_title: str
    status: str
    approved_at: datetime | None
    estimated_budget: Decimal | None
    proposal_owner: ProjectUserResponse | None

    model_config = ConfigDict(from_attributes=True)


class ProjectDetail(BaseModel):
    id: uuid.UUID
    project_number: str
    client_id: uuid.UUID
    proposal_id: uuid.UUID
    project_name: str
    research_type: str | None
    project_value: Decimal | None
    status: str
    notes: str | None
    created_at: datetime
    updated_at: datetime
    ready_at: datetime | None
    business_development_owner: ProjectUserResponse | None
    project_manager: ProjectUserResponse | None
    client: ProjectClientSummary
    proposal: ProjectProposalSummary

    model_config = ConfigDict(from_attributes=True)
