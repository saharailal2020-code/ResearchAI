import uuid

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from app.models.client import Client, ClientActivity, ClientContact
from app.models.user import User
from app.schemas.client import ClientCreate


def create_client(db: Session, payload: ClientCreate, current_user: User) -> Client:
    client = Client(
        client_name=payload.client_name.strip(),
        logo_url=payload.logo_url,
        address=payload.address,
        city=payload.city,
        province=payload.province,
        country=payload.country,
        website=payload.website,
        industry=payload.industry,
        client_type=payload.client_type,
        status=payload.status or "Prospect",
        next_follow_up_at=payload.next_follow_up_at,
        customer_since=payload.customer_since,
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
            mobile_phone=payload.primary_contact.mobile_phone,
            whatsapp_number=payload.primary_contact.whatsapp_number,
            contact_type=payload.primary_contact.contact_type,
            is_primary=payload.primary_contact.is_primary,
            is_decision_maker=payload.primary_contact.is_decision_maker,
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


def list_client_activities(db: Session, client_id: uuid.UUID) -> list[ClientActivity]:
    statement = (
        select(ClientActivity)
        .where(ClientActivity.client_id == client_id)
        .order_by(ClientActivity.activity_at.desc())
    )
    return list(db.execute(statement).scalars().all())
