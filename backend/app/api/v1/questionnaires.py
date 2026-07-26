import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.questionnaire import (
    QuestionnaireCreate,
    QuestionnaireDetail,
    QuestionnaireStatusUpdate,
    QuestionnaireUpdate,
)
from app.services.questionnaires import (
    create_questionnaire,
    get_questionnaire_by_id,
    get_questionnaire_by_project_id,
    list_questionnaires_by_project_id,
    update_questionnaire,
    update_questionnaire_status,
)

router = APIRouter(tags=["questionnaires"])


@router.get("/projects/{project_id}/questionnaires", response_model=list[QuestionnaireDetail])
def get_project_questionnaires(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[QuestionnaireDetail]:
    return list_questionnaires_by_project_id(db, project_id)


@router.post("/projects/{project_id}/questionnaires", response_model=QuestionnaireDetail, status_code=status.HTTP_201_CREATED)
def post_project_questionnaires(
    project_id: uuid.UUID,
    payload: QuestionnaireCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionnaireDetail:
    return create_questionnaire(db, project_id, payload, current_user)


@router.get("/projects/{project_id}/questionnaire", response_model=QuestionnaireDetail | None)
def get_project_questionnaire(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionnaireDetail | None:
    return get_questionnaire_by_project_id(db, project_id)


@router.post("/projects/{project_id}/questionnaire", response_model=QuestionnaireDetail, status_code=status.HTTP_201_CREATED)
def post_project_questionnaire(
    project_id: uuid.UUID,
    payload: QuestionnaireCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionnaireDetail:
    return create_questionnaire(db, project_id, payload, current_user)


@router.get("/questionnaires/{questionnaire_id}", response_model=QuestionnaireDetail)
def get_questionnaire(
    questionnaire_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionnaireDetail:
    questionnaire = get_questionnaire_by_id(db, questionnaire_id)
    if questionnaire is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found")
    return questionnaire


@router.patch("/questionnaires/{questionnaire_id}", response_model=QuestionnaireDetail)
def patch_questionnaire(
    questionnaire_id: uuid.UUID,
    payload: QuestionnaireUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionnaireDetail:
    questionnaire = update_questionnaire(db, questionnaire_id, payload, current_user)
    if questionnaire is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found")
    return questionnaire


@router.patch("/questionnaires/{questionnaire_id}/status", response_model=QuestionnaireDetail)
def patch_questionnaire_status(
    questionnaire_id: uuid.UUID,
    payload: QuestionnaireStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuestionnaireDetail:
    questionnaire = update_questionnaire_status(db, questionnaire_id, payload, current_user)
    if questionnaire is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found")
    return questionnaire
