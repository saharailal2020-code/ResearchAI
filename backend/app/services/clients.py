import uuid
from datetime import datetime

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from app.models.client import Client, ClientActivity, ClientContact
from app.models.user import User
from app.schemas.client import ClientContactCreate, ClientContactUpdate, ClientCreate


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


def record_client_activity(
    db: Session,
    client: Client,
    current_user: User,
    activity_title: str,
    activity_description: str | None = None,
    source_id: uuid.UUID | None = None,
) -> None:
    now = datetime.utcnow()
    client.last_activity_at = now
    db.add(
        ClientActivity(
            client_id=client.id,
            activity_type="Contact",
            activity_title=activity_title,
            activity_description=activity_description,
            source_type="ClientContact",
            source_id=source_id,
            activity_at=now,
            created_by=current_user.id,
        )
    )


def unset_other_primary_contacts(db: Session, client_id: uuid.UUID, contact_id: uuid.UUID | None = None) -> None:
    statement = select(ClientContact).where(ClientContact.client_id == client_id)
    if contact_id is not None:
        statement = statement.where(ClientContact.id != contact_id)

    for contact in db.execute(statement).scalars().all():
        if contact.is_primary:
            contact.is_primary = False


def get_contact_or_none(db: Session, client_id: uuid.UUID, contact_id: uuid.UUID) -> ClientContact | None:
    statement = select(ClientContact).where(
        ClientContact.client_id == client_id,
        ClientContact.id == contact_id,
    )
    return db.execute(statement).scalar_one_or_none()


def create_client_contact(
    db: Session,
    client_id: uuid.UUID,
    payload: ClientContactCreate,
    current_user: User,
) -> ClientContact | None:
    client = get_client_by_id(db, client_id)
    if client is None:
        return None

    if payload.is_primary:
        unset_other_primary_contacts(db, client_id)

    contact = ClientContact(
        client_id=client_id,
        contact_name=payload.contact_name.strip(),
        position=payload.position,
        email=str(payload.email) if payload.email else None,
        phone=payload.phone,
        mobile_phone=payload.mobile_phone,
        whatsapp_number=payload.whatsapp_number,
        contact_type=payload.contact_type,
        is_primary=payload.is_primary,
        is_decision_maker=payload.is_decision_maker,
        notes=payload.notes,
    )
    db.add(contact)
    db.flush()
    record_client_activity(
        db,
        client,
        current_user,
        "Contact person ditambahkan",
        f"{contact.contact_name} ditambahkan sebagai contact person client.",
        contact.id,
    )
    db.commit()
    db.refresh(contact)
    return contact


def update_client_contact(
    db: Session,
    client_id: uuid.UUID,
    contact_id: uuid.UUID,
    payload: ClientContactUpdate,
    current_user: User,
) -> ClientContact | None:
    client = get_client_by_id(db, client_id)
    if client is None:
        return None

    contact = get_contact_or_none(db, client_id, contact_id)
    if contact is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if "contact_name" in update_data and update_data["contact_name"] is not None:
        update_data["contact_name"] = update_data["contact_name"].strip()
    if "email" in update_data and update_data["email"] is not None:
        update_data["email"] = str(update_data["email"])
    if update_data.get("is_primary") is True:
        unset_other_primary_contacts(db, client_id, contact_id)

    for field, value in update_data.items():
        setattr(contact, field, value)

    record_client_activity(
        db,
        client,
        current_user,
        "Contact person diperbarui",
        f"Detail contact person {contact.contact_name} telah diperbarui.",
        contact.id,
    )
    db.commit()
    db.refresh(contact)
    return contact


def set_primary_client_contact(
    db: Session,
    client_id: uuid.UUID,
    contact_id: uuid.UUID,
    current_user: User,
) -> ClientContact | None:
    contact = get_contact_or_none(db, client_id, contact_id)
    if contact is None:
        return None
    return update_client_contact(
        db,
        client_id,
        contact_id,
        ClientContactUpdate(is_primary=True),
        current_user,
    )


def delete_client_contact(
    db: Session,
    client_id: uuid.UUID,
    contact_id: uuid.UUID,
    current_user: User,
) -> bool:
    client = get_client_by_id(db, client_id)
    if client is None:
        return False

    contact = get_contact_or_none(db, client_id, contact_id)
    if contact is None:
        return False

    contact_name = contact.contact_name
    db.delete(contact)
    record_client_activity(
        db,
        client,
        current_user,
        "Contact person dihapus",
        f"{contact_name} dihapus dari daftar contact person client.",
        contact_id,
    )
    db.commit()
    return True


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
