from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class ClientContactCreate(BaseModel):
    contact_name: str
    position: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    is_primary: bool = True
    notes: str | None = None


class ClientCreate(BaseModel):
    client_name: str
    industry: str | None = None
    client_type: str | None = "prospect"
    notes: str | None = None
    primary_contact: ClientContactCreate | None = None


class ClientContactResponse(BaseModel):
    id: uuid.UUID
    contact_name: str
    position: str | None
    email: str | None
    phone: str | None
    is_primary: bool
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientListItem(BaseModel):
    id: uuid.UUID
    client_name: str
    industry: str | None
    client_type: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientDetail(BaseModel):
    id: uuid.UUID
    client_name: str
    industry: str | None
    client_type: str | None
    status: str
    notes: str | None
    contacts: list[ClientContactResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
