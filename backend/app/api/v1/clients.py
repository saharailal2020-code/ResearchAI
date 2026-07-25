import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.client import (
    ClientActivityResponse,
    ClientContactCreate,
    ClientContactResponse,
    ClientContactUpdate,
    ClientCreate,
    ClientDetail,
    ClientListItem,
)
from app.services.clients import (
    create_client,
    create_client_contact,
    delete_client_contact,
    get_client_by_id,
    list_client_activities,
    list_clients,
    set_primary_client_contact,
    update_client_contact,
)

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=list[ClientListItem])
def get_clients(
    search: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ClientListItem]:
    return list_clients(db, search=search, status=status_filter)


@router.post("", response_model=ClientDetail, status_code=status.HTTP_201_CREATED)
def post_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClientDetail:
    return create_client(db, payload, current_user)


@router.get("/{client_id}", response_model=ClientDetail)
def get_client(
    client_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClientDetail:
    client = get_client_by_id(db, client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    return client


@router.get("/{client_id}/activities", response_model=list[ClientActivityResponse])
def get_client_activities(
    client_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ClientActivityResponse]:
    client = get_client_by_id(db, client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    return list_client_activities(db, client_id)


@router.post("/{client_id}/contacts", response_model=ClientContactResponse, status_code=status.HTTP_201_CREATED)
def post_client_contact(
    client_id: uuid.UUID,
    payload: ClientContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClientContactResponse:
    contact = create_client_contact(db, client_id, payload, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )
    return contact


@router.patch("/{client_id}/contacts/{contact_id}", response_model=ClientContactResponse)
def patch_client_contact(
    client_id: uuid.UUID,
    contact_id: uuid.UUID,
    payload: ClientContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClientContactResponse:
    contact = update_client_contact(db, client_id, contact_id, payload, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client contact not found",
        )
    return contact


@router.patch("/{client_id}/contacts/{contact_id}/primary", response_model=ClientContactResponse)
def patch_client_contact_primary(
    client_id: uuid.UUID,
    contact_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ClientContactResponse:
    contact = set_primary_client_contact(db, client_id, contact_id, current_user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client contact not found",
        )
    return contact


@router.delete("/{client_id}/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    client_id: uuid.UUID,
    contact_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    is_deleted = delete_client_contact(db, client_id, contact_id, current_user)
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client contact not found",
        )
