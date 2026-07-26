import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuestionnaireCreate(BaseModel):
    questionnaire_name: str
    target_respondent: str
    instrument_type: str = "Quantitative Survey"
    kobo_link: str | None = None
    xlsform_link: str | None = None


class QuestionnaireUpdate(BaseModel):
    questionnaire_name: str | None = None
    target_respondent: str | None = None
    instrument_type: str | None = None
    kobo_link: str | None = None
    xlsform_link: str | None = None


class QuestionnaireStatusUpdate(BaseModel):
    status: str


class QuestionnaireSummary(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    questionnaire_name: str
    target_respondent: str
    instrument_type: str
    version_number: int
    status: str
    kobo_link: str | None
    xlsform_link: str | None
    sort_order: int
    ready_at: datetime | None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionnaireProjectSummary(BaseModel):
    id: uuid.UUID
    project_number: str
    project_name: str
    status: str
    research_type: str | None

    model_config = ConfigDict(from_attributes=True)


class QuestionnaireDetail(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    questionnaire_name: str
    target_respondent: str
    instrument_type: str
    version_number: int
    status: str
    kobo_link: str | None
    xlsform_link: str | None
    sort_order: int
    ready_at: datetime | None
    created_at: datetime
    updated_at: datetime
    project: QuestionnaireProjectSummary

    model_config = ConfigDict(from_attributes=True)
