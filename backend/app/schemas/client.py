from datetime import datetime
import uuid
import re

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9\s().-]{6,24}$")


def validate_phone_number(value: str | None) -> str | None:
    if value is None or value == "":
        return value
    if not PHONE_PATTERN.match(value):
        raise ValueError("Phone number format is invalid")
    return value


class ClientContactCreate(BaseModel):
    contact_name: str
    position: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    mobile_phone: str | None = None
    whatsapp_number: str | None = None
    contact_type: str | None = None
    is_primary: bool = True
    is_decision_maker: bool = False
    notes: str | None = None

    _validate_phone = field_validator("phone", "mobile_phone", "whatsapp_number")(validate_phone_number)


class ClientContactUpdate(BaseModel):
    contact_name: str | None = None
    position: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    mobile_phone: str | None = None
    whatsapp_number: str | None = None
    contact_type: str | None = None
    is_primary: bool | None = None
    is_decision_maker: bool | None = None
    notes: str | None = None

    _validate_phone = field_validator("phone", "mobile_phone", "whatsapp_number")(validate_phone_number)


class ClientCreate(BaseModel):
    client_name: str
    logo_url: str | None = None
    address: str | None = None
    city: str | None = None
    province: str | None = None
    country: str | None = None
    website: str | None = None
    industry: str | None = None
    client_type: str | None = "Prospect"
    status: str | None = "Prospect"
    next_follow_up_at: datetime | None = None
    customer_since: datetime | None = None
    notes: str | None = None
    primary_contact: ClientContactCreate | None = None


class ClientContactResponse(BaseModel):
    id: uuid.UUID
    contact_name: str
    position: str | None
    email: str | None
    phone: str | None
    mobile_phone: str | None
    whatsapp_number: str | None
    contact_type: str | None
    is_primary: bool
    is_decision_maker: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientActivityResponse(BaseModel):
    id: uuid.UUID
    activity_type: str
    activity_title: str
    activity_description: str | None
    source_type: str | None
    source_id: uuid.UUID | None
    activity_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientListItem(BaseModel):
    id: uuid.UUID
    client_name: str
    logo_url: str | None
    city: str | None
    industry: str | None
    client_type: str | None
    status: str
    last_activity_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientDetail(BaseModel):
    id: uuid.UUID
    client_name: str
    logo_url: str | None
    address: str | None
    city: str | None
    province: str | None
    country: str | None
    website: str | None
    industry: str | None
    client_type: str | None
    status: str
    last_activity_at: datetime | None
    next_follow_up_at: datetime | None
    customer_since: datetime | None
    notes: str | None
    contacts: list[ClientContactResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
