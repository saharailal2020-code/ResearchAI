import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SamplingTargetCreate(BaseModel):
    region_type: str
    region_name: str
    target_sample: int


class SamplingTargetUpdate(BaseModel):
    region_type: str | None = None
    region_name: str | None = None
    target_sample: int | None = None


class SamplingTargetResponse(BaseModel):
    id: uuid.UUID
    sample_group_id: uuid.UUID
    region_type: str
    region_name: str
    target_sample: int
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SampleGroupCreate(BaseModel):
    questionnaire_id: uuid.UUID | None = None
    sample_group_name: str
    target_respondent: str | None = None
    notes: str | None = None
    targets: list[SamplingTargetCreate]


class SampleGroupUpdate(BaseModel):
    questionnaire_id: uuid.UUID | None = None
    sample_group_name: str | None = None
    target_respondent: str | None = None
    notes: str | None = None
    targets: list[SamplingTargetCreate] | None = None


class SampleGroupStatusUpdate(BaseModel):
    status: str


class SampleGroupQuestionnaireSummary(BaseModel):
    id: uuid.UUID
    questionnaire_name: str
    target_respondent: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class SampleGroupProjectSummary(BaseModel):
    id: uuid.UUID
    project_number: str
    project_name: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class SampleGroupDetail(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    questionnaire_id: uuid.UUID | None
    sample_group_name: str
    target_respondent: str | None
    total_target_sample: int
    status: str
    notes: str | None
    sort_order: int
    ready_at: datetime | None
    created_at: datetime
    updated_at: datetime
    project: SampleGroupProjectSummary
    questionnaire: SampleGroupQuestionnaireSummary | None
    targets: list[SamplingTargetResponse]

    model_config = ConfigDict(from_attributes=True)
