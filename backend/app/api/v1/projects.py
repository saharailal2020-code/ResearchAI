import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.project import ProjectDetail, ProjectSetupCreate, ProjectStatusUpdate
from app.services.projects import get_project_by_id, setup_project_from_proposal, update_project_status

router = APIRouter(tags=["projects"])


@router.post("/proposals/{proposal_id}/setup-project", response_model=ProjectDetail, status_code=status.HTTP_201_CREATED)
def post_setup_project(
    proposal_id: uuid.UUID,
    payload: ProjectSetupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectDetail:
    return setup_project_from_proposal(db, proposal_id, payload, current_user)


@router.get("/projects/{project_id}", response_model=ProjectDetail)
def get_project(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectDetail:
    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/projects/{project_id}/status", response_model=ProjectDetail)
def patch_project_status(
    project_id: uuid.UUID,
    payload: ProjectStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectDetail:
    project = update_project_status(db, project_id, payload, current_user)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project
