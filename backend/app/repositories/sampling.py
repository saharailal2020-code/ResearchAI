import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.project import Project
from app.models.questionnaire import Questionnaire
from app.models.sampling import SampleGroup, SamplingTarget


def get_project(db: Session, project_id: uuid.UUID) -> Project | None:
    return db.get(Project, project_id)


def get_questionnaire(db: Session, questionnaire_id: uuid.UUID) -> Questionnaire | None:
    return db.get(Questionnaire, questionnaire_id)


def get_sample_group_by_id(db: Session, sample_group_id: uuid.UUID) -> SampleGroup | None:
    statement = (
        select(SampleGroup)
        .options(
            joinedload(SampleGroup.project).joinedload(Project.client),
            joinedload(SampleGroup.questionnaire),
            joinedload(SampleGroup.targets),
        )
        .where(SampleGroup.id == sample_group_id)
    )
    return db.execute(statement).unique().scalar_one_or_none()


def list_sample_groups_by_project_id(db: Session, project_id: uuid.UUID) -> list[SampleGroup]:
    statement = (
        select(SampleGroup)
        .options(joinedload(SampleGroup.questionnaire), joinedload(SampleGroup.targets))
        .where(SampleGroup.project_id == project_id)
        .order_by(SampleGroup.sort_order.asc(), SampleGroup.created_at.asc())
    )
    return list(db.execute(statement).unique().scalars().all())


def get_sampling_target_by_id(db: Session, target_id: uuid.UUID) -> SamplingTarget | None:
    statement = (
        select(SamplingTarget)
        .options(
            joinedload(SamplingTarget.sample_group)
            .joinedload(SampleGroup.project)
            .joinedload(Project.client),
            joinedload(SamplingTarget.sample_group).joinedload(SampleGroup.questionnaire),
            joinedload(SamplingTarget.sample_group).joinedload(SampleGroup.targets),
        )
        .where(SamplingTarget.id == target_id)
    )
    return db.execute(statement).unique().scalar_one_or_none()


def list_sampling_targets_by_sample_group_id(db: Session, sample_group_id: uuid.UUID) -> list[SamplingTarget]:
    statement = (
        select(SamplingTarget)
        .where(SamplingTarget.sample_group_id == sample_group_id)
        .order_by(SamplingTarget.sort_order.asc(), SamplingTarget.created_at.asc())
    )
    return list(db.execute(statement).scalars().all())


def get_next_sample_group_sort_order(db: Session, project_id: uuid.UUID) -> int:
    max_order = db.execute(
        select(func.max(SampleGroup.sort_order)).where(SampleGroup.project_id == project_id)
    ).scalar_one()
    return int(max_order or 0) + 1


def get_next_sampling_target_sort_order(db: Session, sample_group_id: uuid.UUID) -> int:
    max_order = db.execute(
        select(func.max(SamplingTarget.sort_order)).where(SamplingTarget.sample_group_id == sample_group_id)
    ).scalar_one()
    return int(max_order or 0) + 1


def build_sampling_targets(sample_group_id: uuid.UUID, target_rows: list[dict[str, object]]) -> list[SamplingTarget]:
    return [
        SamplingTarget(
            sample_group_id=sample_group_id,
            region_type=str(target["region_type"]),
            region_name=str(target["region_name"]),
            target_sample=int(target["target_sample"]),
            sort_order=index,
        )
        for index, target in enumerate(target_rows, start=1)
    ]
