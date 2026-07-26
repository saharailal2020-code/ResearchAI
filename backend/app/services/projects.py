import uuid
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.client import ClientActivity
from app.models.project import Project
from app.models.proposal import Proposal
from app.models.user import User
from app.schemas.project import ProjectSetupCreate, ProjectStatusUpdate

ALLOWED_PROJECT_STATUSES = {"Setup", "Ready", "Fieldwork", "QC", "Analysis", "Reporting", "Completed", "Cancelled"}


def generate_project_number(db: Session) -> str:
    today_key = datetime.utcnow().strftime("%Y%m%d")
    prefix = f"PRJ-{today_key}"
    count_statement = select(func.count()).select_from(Project).where(Project.project_number.like(f"{prefix}-%"))
    sequence = int(db.execute(count_statement).scalar_one()) + 1

    while True:
        project_number = f"{prefix}-{sequence:04d}"
        existing = db.execute(select(Project.id).where(Project.project_number == project_number)).scalar_one_or_none()
        if existing is None:
            return project_number
        sequence += 1


def get_project_by_id(db: Session, project_id: uuid.UUID) -> Project | None:
    statement = (
        select(Project)
        .options(
            joinedload(Project.client),
            joinedload(Project.proposal).joinedload(Proposal.proposal_owner),
            joinedload(Project.business_development_owner),
            joinedload(Project.project_manager),
        )
        .where(Project.id == project_id)
    )
    return db.execute(statement).scalar_one_or_none()


def get_project_by_proposal_id(db: Session, proposal_id: uuid.UUID) -> Project | None:
    statement = (
        select(Project)
        .options(
            joinedload(Project.client),
            joinedload(Project.proposal).joinedload(Proposal.proposal_owner),
            joinedload(Project.business_development_owner),
            joinedload(Project.project_manager),
        )
        .where(Project.proposal_id == proposal_id)
    )
    return db.execute(statement).scalar_one_or_none()


def record_project_activity(
    db: Session,
    project: Project,
    current_user: User,
    activity_title: str,
    activity_description: str,
) -> None:
    now = datetime.utcnow()
    project.client.last_activity_at = now
    db.add(
        ClientActivity(
            client_id=project.client_id,
            activity_type="Project",
            activity_title=activity_title,
            activity_description=activity_description,
            source_type="Project",
            source_id=project.id,
            activity_at=now,
            created_by=current_user.id,
        )
    )


def setup_project_from_proposal(
    db: Session,
    proposal_id: uuid.UUID,
    payload: ProjectSetupCreate,
    current_user: User,
) -> Project:
    proposal = db.execute(
        select(Proposal)
        .options(joinedload(Proposal.client), joinedload(Proposal.proposal_owner), joinedload(Proposal.project))
        .where(Proposal.id == proposal_id)
    ).scalar_one_or_none()
    if proposal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found")
    if proposal.status != "Approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project can only be created from an approved proposal",
        )

    existing_project = get_project_by_proposal_id(db, proposal_id)
    if existing_project is not None:
        return existing_project

    project_name = payload.project_name.strip()
    if len(project_name) < 3:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Project name is required")

    project = Project(
        project_number=generate_project_number(db),
        client_id=proposal.client_id,
        proposal_id=proposal.id,
        project_name=project_name,
        research_type=proposal.research_type,
        project_value=proposal.estimated_budget,
        business_development_owner_id=proposal.proposal_owner_id,
        status="Setup",
        created_by=current_user.id,
    )
    db.add(project)
    db.flush()
    project.client = proposal.client
    project.proposal = proposal
    project.business_development_owner = proposal.proposal_owner
    record_project_activity(
        db,
        project,
        current_user,
        "Project dibuat dari Proposal",
        f"Project {project.project_name} dibuat dari Proposal {proposal.proposal_number}.",
    )
    db.commit()
    db.refresh(project)
    return get_project_by_id(db, project.id)


def update_project_status(
    db: Session,
    project_id: uuid.UUID,
    payload: ProjectStatusUpdate,
    current_user: User,
) -> Project | None:
    project = get_project_by_id(db, project_id)
    if project is None:
        return None
    if payload.status not in ALLOWED_PROJECT_STATUSES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid project status")
    if project.status == payload.status:
        return project
    if project.status != "Setup" or payload.status != "Ready":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Setup to Ready transition is available in this sprint",
        )

    project.status = "Ready"
    project.ready_at = datetime.utcnow()
    record_project_activity(
        db,
        project,
        current_user,
        "Project ditandai Ready",
        f"Project {project.project_name} siap dijalankan.",
    )
    db.commit()
    db.refresh(project)
    return get_project_by_id(db, project.id)
