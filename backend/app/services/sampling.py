import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.client import ClientActivity
from app.models.project import Project
from app.models.sampling import SampleGroup, SamplingTarget
from app.models.user import User
from app.repositories.sampling import (
    build_sampling_targets,
    get_next_sample_group_sort_order,
    get_next_sampling_target_sort_order,
    get_project,
    get_questionnaire,
    get_sample_group_by_id,
    get_sampling_target_by_id,
    list_sample_groups_by_project_id as repository_list_sample_groups_by_project_id,
    list_sampling_targets_by_sample_group_id as repository_list_sampling_targets_by_sample_group_id,
)
from app.schemas.sampling import (
    SampleGroupCreate,
    SampleGroupStatusUpdate,
    SampleGroupUpdate,
    SamplingTargetCreate,
    SamplingTargetUpdate,
)

ALLOWED_SAMPLE_GROUP_STATUSES = {"Draft", "Ready"}
BLOCKED_PROJECT_STATUSES = {"Completed", "Cancelled"}


def validate_text(value: str | None, field_name: str, min_length: int = 2, max_length: int = 200) -> str:
    cleaned_value = (value or "").strip()
    if len(cleaned_value) < min_length:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{field_name} is required")
    if len(cleaned_value) > max_length:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be {max_length} characters or fewer",
        )
    return cleaned_value


def clean_optional_text(value: str | None, max_length: int = 500) -> str | None:
    if value is None:
        return None
    cleaned_value = value.strip()
    if not cleaned_value:
        return None
    if len(cleaned_value) > max_length:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Text must be {max_length} characters or fewer",
        )
    return cleaned_value


def validate_targets(targets: list[SamplingTargetCreate]) -> list[dict[str, object]]:
    if not targets:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one sampling target is required",
        )

    cleaned_targets: list[dict[str, object]] = []
    for target in targets:
        region_type = validate_text(target.region_type, "Region type", max_length=80)
        region_name = validate_text(target.region_name, "Region name", max_length=150)
        if target.target_sample <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Target sample must be greater than 0",
            )
        cleaned_targets.append(
            {
                "region_type": region_type,
                "region_name": region_name,
                "target_sample": target.target_sample,
            }
        )
    return cleaned_targets


def calculate_total_target_sample(target_rows: list[dict[str, object]]) -> int:
    return sum(int(target["target_sample"]) for target in target_rows)


def recalculate_sample_group_total(sample_group: SampleGroup) -> None:
    sample_group.total_target_sample = sum(target.target_sample for target in sample_group.targets)


def ensure_project_allows_sampling(project: Project) -> None:
    if project.status in BLOCKED_PROJECT_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sampling Plan cannot be changed for completed or cancelled projects",
        )


def validate_questionnaire_for_project(
    db: Session,
    questionnaire_id: uuid.UUID | None,
    project_id: uuid.UUID,
) -> uuid.UUID | None:
    if questionnaire_id is None:
        return None

    questionnaire = get_questionnaire(db, questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found")
    if questionnaire.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questionnaire must belong to the same project",
        )
    return questionnaire.id


def record_sampling_activity(
    db: Session,
    sample_group: SampleGroup,
    current_user: User,
    activity_title: str,
    activity_description: str,
) -> None:
    now = datetime.utcnow()
    sample_group.project.client.last_activity_at = now
    db.add(
        ClientActivity(
            client_id=sample_group.project.client_id,
            activity_type="SamplingPlan",
            activity_title=activity_title,
            activity_description=activity_description,
            source_type="SamplingPlan",
            source_id=sample_group.id,
            activity_at=now,
            created_by=current_user.id,
        )
    )


def create_sample_group(
    db: Session,
    project_id: uuid.UUID,
    payload: SampleGroupCreate,
    current_user: User,
) -> SampleGroup:
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    ensure_project_allows_sampling(project)

    questionnaire_id = validate_questionnaire_for_project(db, payload.questionnaire_id, project_id)
    target_rows = validate_targets(payload.targets)
    sample_group = SampleGroup(
        project_id=project_id,
        questionnaire_id=questionnaire_id,
        sample_group_name=validate_text(payload.sample_group_name, "Sample group name"),
        target_respondent=clean_optional_text(payload.target_respondent, max_length=150),
        total_target_sample=calculate_total_target_sample(target_rows),
        status="Draft",
        notes=clean_optional_text(payload.notes, max_length=1000),
        sort_order=get_next_sample_group_sort_order(db, project_id),
        created_by=current_user.id,
    )
    db.add(sample_group)
    db.flush()
    sample_group.targets = build_sampling_targets(sample_group.id, target_rows)
    sample_group.project = db.query(Project).options(joinedload(Project.client)).filter(Project.id == project_id).one()
    record_sampling_activity(
        db,
        sample_group,
        current_user,
        "Sampling Plan dibuat",
        f"Sample Group {sample_group.sample_group_name} telah dibuat.",
    )
    db.commit()
    return get_sample_group_by_id(db, sample_group.id)


def list_sample_groups_by_project(db: Session, project_id: uuid.UUID) -> list[SampleGroup]:
    project = get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return repository_list_sample_groups_by_project_id(db, project_id)


def get_sample_group_detail(db: Session, sample_group_id: uuid.UUID) -> SampleGroup | None:
    return get_sample_group_by_id(db, sample_group_id)


def update_sample_group(
    db: Session,
    sample_group_id: uuid.UUID,
    payload: SampleGroupUpdate,
    current_user: User,
) -> SampleGroup | None:
    sample_group = get_sample_group_by_id(db, sample_group_id)
    if sample_group is None:
        return None
    ensure_project_allows_sampling(sample_group.project)
    if sample_group.status != "Draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ready sample group cannot be edited",
        )

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        return sample_group

    if "questionnaire_id" in update_data:
        sample_group.questionnaire_id = validate_questionnaire_for_project(
            db,
            update_data["questionnaire_id"],
            sample_group.project_id,
        )
    if "sample_group_name" in update_data and update_data["sample_group_name"] is not None:
        sample_group.sample_group_name = validate_text(update_data["sample_group_name"], "Sample group name")
    if "target_respondent" in update_data:
        sample_group.target_respondent = clean_optional_text(update_data["target_respondent"], max_length=150)
    if "notes" in update_data:
        sample_group.notes = clean_optional_text(update_data["notes"], max_length=1000)
    if "targets" in update_data and update_data["targets"] is not None:
        target_rows = validate_targets(payload.targets or [])
        sample_group.targets = build_sampling_targets(sample_group.id, target_rows)
        sample_group.total_target_sample = calculate_total_target_sample(target_rows)

    record_sampling_activity(
        db,
        sample_group,
        current_user,
        "Sampling Plan diperbarui",
        f"Sample Group {sample_group.sample_group_name} telah diperbarui.",
    )
    db.commit()
    return get_sample_group_by_id(db, sample_group.id)


def delete_sample_group(db: Session, sample_group_id: uuid.UUID, current_user: User) -> bool:
    sample_group = get_sample_group_by_id(db, sample_group_id)
    if sample_group is None:
        return False
    ensure_project_allows_sampling(sample_group.project)
    if sample_group.status != "Draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ready sample group cannot be deleted",
        )

    record_sampling_activity(
        db,
        sample_group,
        current_user,
        "Sampling Plan dihapus",
        f"Sample Group {sample_group.sample_group_name} telah dihapus.",
    )
    db.delete(sample_group)
    db.commit()
    return True


def update_sample_group_status(
    db: Session,
    sample_group_id: uuid.UUID,
    payload: SampleGroupStatusUpdate,
    current_user: User,
) -> SampleGroup | None:
    sample_group = get_sample_group_by_id(db, sample_group_id)
    if sample_group is None:
        return None
    ensure_project_allows_sampling(sample_group.project)
    if payload.status not in ALLOWED_SAMPLE_GROUP_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sample group status")
    if sample_group.status == payload.status:
        return sample_group
    if sample_group.status != "Draft" or payload.status != "Ready":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Draft to Ready transition is available in this sprint",
        )
    if not sample_group.targets or sample_group.total_target_sample <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Sample group must have at least one sampling target before Ready",
        )

    sample_group.status = "Ready"
    sample_group.ready_at = datetime.utcnow()
    record_sampling_activity(
        db,
        sample_group,
        current_user,
        "Sampling Plan ditandai Ready",
        f"Sample Group {sample_group.sample_group_name} siap digunakan untuk Fieldwork.",
    )
    db.commit()
    return get_sample_group_by_id(db, sample_group.id)


def list_sampling_targets_by_sample_group(db: Session, sample_group_id: uuid.UUID) -> list[SamplingTarget]:
    sample_group = get_sample_group_by_id(db, sample_group_id)
    if sample_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample group not found")
    return repository_list_sampling_targets_by_sample_group_id(db, sample_group_id)


def get_sampling_target_detail(db: Session, target_id: uuid.UUID) -> SamplingTarget | None:
    return get_sampling_target_by_id(db, target_id)


def create_sampling_target(
    db: Session,
    sample_group_id: uuid.UUID,
    payload: SamplingTargetCreate,
    current_user: User,
) -> SampleGroup | None:
    sample_group = get_sample_group_by_id(db, sample_group_id)
    if sample_group is None:
        return None
    ensure_project_allows_sampling(sample_group.project)
    if sample_group.status != "Draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ready sample group cannot be edited",
        )

    target_row = validate_targets([payload])[0]
    sample_group.targets.append(
        SamplingTarget(
            sample_group_id=sample_group.id,
            region_type=str(target_row["region_type"]),
            region_name=str(target_row["region_name"]),
            target_sample=int(target_row["target_sample"]),
            sort_order=get_next_sampling_target_sort_order(db, sample_group.id),
        )
    )
    db.flush()
    recalculate_sample_group_total(sample_group)
    record_sampling_activity(
        db,
        sample_group,
        current_user,
        "Sampling Plan diperbarui",
        f"Sample Group {sample_group.sample_group_name} telah diperbarui.",
    )
    db.commit()
    return get_sample_group_by_id(db, sample_group.id)


def update_sampling_target(
    db: Session,
    target_id: uuid.UUID,
    payload: SamplingTargetUpdate,
    current_user: User,
) -> SampleGroup | None:
    target = get_sampling_target_by_id(db, target_id)
    if target is None:
        return None
    sample_group = target.sample_group
    ensure_project_allows_sampling(sample_group.project)
    if sample_group.status != "Draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ready sample group cannot be edited",
        )

    update_data = payload.model_dump(exclude_unset=True)
    if "region_type" in update_data and update_data["region_type"] is not None:
        target.region_type = validate_text(update_data["region_type"], "Region type", max_length=80)
    if "region_name" in update_data and update_data["region_name"] is not None:
        target.region_name = validate_text(update_data["region_name"], "Region name", max_length=150)
    if "target_sample" in update_data and update_data["target_sample"] is not None:
        if update_data["target_sample"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Target sample must be greater than 0",
            )
        target.target_sample = update_data["target_sample"]

    refreshed_sample_group = get_sample_group_by_id(db, sample_group.id)
    recalculate_sample_group_total(refreshed_sample_group)
    record_sampling_activity(
        db,
        refreshed_sample_group,
        current_user,
        "Sampling Plan diperbarui",
        f"Sample Group {refreshed_sample_group.sample_group_name} telah diperbarui.",
    )
    db.commit()
    return get_sample_group_by_id(db, sample_group.id)


def delete_sampling_target(db: Session, target_id: uuid.UUID, current_user: User) -> SampleGroup | None:
    target = get_sampling_target_by_id(db, target_id)
    if target is None:
        return None
    sample_group = target.sample_group
    ensure_project_allows_sampling(sample_group.project)
    if sample_group.status != "Draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ready sample group cannot be edited",
        )
    if len(sample_group.targets) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sample group must have at least one sampling target",
        )

    sample_group.targets.remove(target)
    db.delete(target)
    db.flush()
    recalculate_sample_group_total(sample_group)
    record_sampling_activity(
        db,
        sample_group,
        current_user,
        "Sampling Plan diperbarui",
        f"Sample Group {sample_group.sample_group_name} telah diperbarui.",
    )
    db.commit()
    return get_sample_group_by_id(db, sample_group.id)


__all__ = [
    "create_sample_group",
    "create_sampling_target",
    "delete_sample_group",
    "delete_sampling_target",
    "get_sample_group_detail",
    "get_sampling_target_detail",
    "list_sample_groups_by_project",
    "list_sampling_targets_by_sample_group",
    "update_sample_group",
    "update_sample_group_status",
    "update_sampling_target",
]
