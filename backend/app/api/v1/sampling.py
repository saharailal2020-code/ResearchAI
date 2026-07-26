import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.sampling import (
    SampleGroupCreate,
    SampleGroupDetail,
    SampleGroupStatusUpdate,
    SampleGroupUpdate,
    SamplingTargetCreate,
    SamplingTargetResponse,
    SamplingTargetUpdate,
)
from app.services.sampling import (
    create_sample_group,
    create_sampling_target,
    delete_sample_group,
    delete_sampling_target,
    get_sample_group_detail,
    get_sampling_target_detail,
    list_sample_groups_by_project,
    list_sampling_targets_by_sample_group,
    update_sample_group,
    update_sample_group_status,
    update_sampling_target,
)

router = APIRouter(tags=["sampling-plan"])


@router.get("/projects/{project_id}/sample-groups", response_model=list[SampleGroupDetail])
def get_project_sample_groups(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[SampleGroupDetail]:
    return list_sample_groups_by_project(db, project_id)


@router.post(
    "/projects/{project_id}/sample-groups",
    response_model=SampleGroupDetail,
    status_code=status.HTTP_201_CREATED,
)
def post_project_sample_group(
    project_id: uuid.UUID,
    payload: SampleGroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SampleGroupDetail:
    return create_sample_group(db, project_id, payload, current_user)


@router.get("/sample-groups/{sample_group_id}", response_model=SampleGroupDetail)
def get_sample_group(
    sample_group_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SampleGroupDetail:
    sample_group = get_sample_group_detail(db, sample_group_id)
    if sample_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample group not found")
    return sample_group


@router.patch("/sample-groups/{sample_group_id}", response_model=SampleGroupDetail)
def patch_sample_group(
    sample_group_id: uuid.UUID,
    payload: SampleGroupUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SampleGroupDetail:
    sample_group = update_sample_group(db, sample_group_id, payload, current_user)
    if sample_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample group not found")
    return sample_group


@router.delete("/sample-groups/{sample_group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample_group_endpoint(
    sample_group_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    deleted = delete_sample_group(db, sample_group_id, current_user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample group not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/sample-groups/{sample_group_id}/status", response_model=SampleGroupDetail)
def patch_sample_group_status(
    sample_group_id: uuid.UUID,
    payload: SampleGroupStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SampleGroupDetail:
    sample_group = update_sample_group_status(db, sample_group_id, payload, current_user)
    if sample_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample group not found")
    return sample_group


@router.get("/sample-groups/{sample_group_id}/targets", response_model=list[SamplingTargetResponse])
def get_sample_group_targets(
    sample_group_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[SamplingTargetResponse]:
    return list_sampling_targets_by_sample_group(db, sample_group_id)


@router.post(
    "/sample-groups/{sample_group_id}/targets",
    response_model=SampleGroupDetail,
    status_code=status.HTTP_201_CREATED,
)
def post_sample_group_target(
    sample_group_id: uuid.UUID,
    payload: SamplingTargetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SampleGroupDetail:
    sample_group = create_sampling_target(db, sample_group_id, payload, current_user)
    if sample_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample group not found")
    return sample_group


@router.get("/sampling-targets/{target_id}", response_model=SamplingTargetResponse)
def get_sampling_target(
    target_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SamplingTargetResponse:
    target = get_sampling_target_detail(db, target_id)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sampling target not found")
    return target


@router.patch("/sampling-targets/{target_id}", response_model=SampleGroupDetail)
def patch_sampling_target(
    target_id: uuid.UUID,
    payload: SamplingTargetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SampleGroupDetail:
    sample_group = update_sampling_target(db, target_id, payload, current_user)
    if sample_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sampling target not found")
    return sample_group


@router.delete("/sampling-targets/{target_id}", response_model=SampleGroupDetail)
def delete_sampling_target_endpoint(
    target_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SampleGroupDetail:
    sample_group = delete_sampling_target(db, target_id, current_user)
    if sample_group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sampling target not found")
    return sample_group
