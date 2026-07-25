import uuid

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from app.models.client import Client, ClientContact
from app.models.user import User
from app.schemas.client import ClientCreate


def create_client(db: Session, payload: ClientCreate, current_user: User) -> Client:
    client = Client(
        client_name=payload.client_name.strip(),
        industry=payload.industry,
        client_type=payload.client_type,
        status="active",
        notes=payload.notes,
        created_by=current_user.id,
    )
    db.add(client)
    db.flush()

    if payload.primary_contact is not None:
        contact = ClientContact(
            client_id=client.id,
            contact_name=payload.primary_contact.contact_name.strip(),
            position=payload.primary_contact.position,
            email=str(payload.primary_contact.email) if payload.primary_contact.email else None,
            phone=payload.primary_contact.phone,
            is_primary=payload.primary_contact.is_primary,
            notes=payload.primary_contact.notes,
        )
        db.add(contact)

    db.commit()
    db.refresh(client)
    return get_client_by_id(db, client.id)


def build_clients_query(search: str | None = None, status: str | None = None) -> Select[tuple[Client]]:
    statement = select(Client)
    if search:
        statement = statement.where(func.lower(Client.client_name).contains(search.lower()))
    if status:
        statement = statement.where(Client.status == status)
    return statement.order_by(Client.created_at.desc())


def list_clients(db: Session, search: str | None = None, status: str | None = None) -> list[Client]:
    return list(db.execute(build_clients_query(search=search, status=status)).scalars().all())


def get_client_by_id(db: Session, client_id: uuid.UUID) -> Client | None:
    statement = (
        select(Client)
        .options(selectinload(Client.contacts))
        .where(Client.id == client_id)
    )
    return db.execute(statement).scalar_one_or_none()
