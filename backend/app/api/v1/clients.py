import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.client import ClientCreate, ClientDetail, ClientListItem
from app.services.clients import create_client, get_client_by_id, list_clients

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
