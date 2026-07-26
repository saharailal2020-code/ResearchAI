import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.client import ClientActivity
from app.models.project import Project
from app.models.questionnaire import Questionnaire
from app.models.user import User
from app.schemas.questionnaire import QuestionnaireCreate, QuestionnaireStatusUpdate, QuestionnaireUpdate

ALLOWED_QUESTIONNAIRE_STATUSES = {"Draft", "Ready"}


def get_questionnaire_by_id(db: Session, questionnaire_id: uuid.UUID) -> Questionnaire | None:
    statement = (
        select(Questionnaire)
        .options(joinedload(Questionnaire.project).joinedload(Project.client))
        .where(Questionnaire.id == questionnaire_id)
    )
    return db.execute(statement).scalar_one_or_none()


def list_questionnaires_by_project_id(db: Session, project_id: uuid.UUID) -> list[Questionnaire]:
    statement = (
        select(Questionnaire)
        .options(joinedload(Questionnaire.project).joinedload(Project.client))
        .where(Questionnaire.project_id == project_id)
        .order_by(Questionnaire.sort_order.asc(), Questionnaire.created_at.asc())
    )
    return list(db.execute(statement).scalars().all())


def get_questionnaire_by_project_id(db: Session, project_id: uuid.UUID) -> Questionnaire | None:
    statement = (
        select(Questionnaire)
        .options(joinedload(Questionnaire.project).joinedload(Project.client))
        .where(Questionnaire.project_id == project_id)
        .order_by(Questionnaire.sort_order.asc(), Questionnaire.created_at.asc())
    )
    return db.execute(statement).scalars().first()


def record_questionnaire_activity(
    db: Session,
    questionnaire: Questionnaire,
    current_user: User,
    activity_title: str,
    activity_description: str,
) -> None:
    now = datetime.utcnow()
    questionnaire.project.client.last_activity_at = now
    db.add(
        ClientActivity(
            client_id=questionnaire.project.client_id,
            activity_type="Questionnaire",
            activity_title=activity_title,
            activity_description=activity_description,
            source_type="Questionnaire",
            source_id=questionnaire.id,
            activity_at=now,
            created_by=current_user.id,
        )
    )


def validate_questionnaire_name(questionnaire_name: str) -> str:
    cleaned_name = questionnaire_name.strip()
    if len(cleaned_name) < 3:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Questionnaire name is required")
    if len(cleaned_name) > 150:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Questionnaire name must be 150 characters or fewer",
        )
    return cleaned_name


def validate_required_text(value: str, field_name: str, max_length: int = 150) -> str:
    cleaned_value = value.strip()
    if len(cleaned_value) < 2:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{field_name} is required")
    if len(cleaned_value) > max_length:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be {max_length} characters or fewer",
        )
    return cleaned_value


def get_next_sort_order(db: Session, project_id: uuid.UUID) -> int:
    max_order = db.execute(
        select(func.max(Questionnaire.sort_order)).where(Questionnaire.project_id == project_id)
    ).scalar_one()
    return int(max_order or 0) + 1


def create_questionnaire(
    db: Session,
    project_id: uuid.UUID,
    payload: QuestionnaireCreate,
    current_user: User,
) -> Questionnaire:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    questionnaire = Questionnaire(
        project_id=project_id,
        questionnaire_name=validate_questionnaire_name(payload.questionnaire_name),
        target_respondent=validate_required_text(payload.target_respondent, "Target respondent"),
        instrument_type=validate_required_text(payload.instrument_type, "Instrument type"),
        version_number=1,
        status="Draft",
        kobo_link=payload.kobo_link,
        xlsform_link=payload.xlsform_link,
        sort_order=get_next_sort_order(db, project_id),
        created_by=current_user.id,
    )
    db.add(questionnaire)
    db.flush()
    questionnaire.project = db.execute(
        select(Project).options(joinedload(Project.client)).where(Project.id == project_id)
    ).scalar_one()
    record_questionnaire_activity(
        db,
        questionnaire,
        current_user,
        "Questionnaire dibuat",
        f"Questionnaire {questionnaire.questionnaire_name} telah dibuat.",
    )
    db.commit()
    db.refresh(questionnaire)
    return get_questionnaire_by_id(db, questionnaire.id)


def update_questionnaire(
    db: Session,
    questionnaire_id: uuid.UUID,
    payload: QuestionnaireUpdate,
    current_user: User,
) -> Questionnaire | None:
    questionnaire = get_questionnaire_by_id(db, questionnaire_id)
    if questionnaire is None:
        return None
    if questionnaire.status != "Draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ready questionnaire cannot be edited",
        )

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        return questionnaire
    if "questionnaire_name" in update_data and update_data["questionnaire_name"] is not None:
        update_data["questionnaire_name"] = validate_questionnaire_name(update_data["questionnaire_name"])
    if "target_respondent" in update_data and update_data["target_respondent"] is not None:
        update_data["target_respondent"] = validate_required_text(update_data["target_respondent"], "Target respondent")
    if "instrument_type" in update_data and update_data["instrument_type"] is not None:
        update_data["instrument_type"] = validate_required_text(update_data["instrument_type"], "Instrument type")

    for field, value in update_data.items():
        setattr(questionnaire, field, value)

    record_questionnaire_activity(
        db,
        questionnaire,
        current_user,
        "Questionnaire diperbarui",
        f"Questionnaire {questionnaire.questionnaire_name} telah diperbarui.",
    )
    db.commit()
    db.refresh(questionnaire)
    return get_questionnaire_by_id(db, questionnaire.id)


def update_questionnaire_status(
    db: Session,
    questionnaire_id: uuid.UUID,
    payload: QuestionnaireStatusUpdate,
    current_user: User,
) -> Questionnaire | None:
    questionnaire = get_questionnaire_by_id(db, questionnaire_id)
    if questionnaire is None:
        return None
    if payload.status not in ALLOWED_QUESTIONNAIRE_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid questionnaire status")
    if questionnaire.status == payload.status:
        return questionnaire
    if questionnaire.status != "Draft" or payload.status != "Ready":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Draft to Ready transition is available in this sprint",
        )

    questionnaire.status = "Ready"
    questionnaire.ready_at = datetime.utcnow()
    record_questionnaire_activity(
        db,
        questionnaire,
        current_user,
        "Questionnaire ditandai Ready",
        f"Questionnaire {questionnaire.questionnaire_name} siap digunakan.",
    )
    db.commit()
    db.refresh(questionnaire)
    return get_questionnaire_by_id(db, questionnaire.id)
