import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(String(250), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    client_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Prospect", index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    next_follow_up_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True, nullable=True)
    customer_since: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    contacts: Mapped[list["ClientContact"]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan",
    )
    proposals: Mapped[list["Proposal"]] = relationship(back_populates="client")
    projects: Mapped[list["Project"]] = relationship(back_populates="client")
    activities: Mapped[list["ClientActivity"]] = relationship(
        back_populates="client",
        cascade="all, delete-orphan",
    )


class ClientContact(Base):
    __tablename__ = "client_contacts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id"), index=True, nullable=False)
    contact_name: Mapped[str] = mapped_column(String(150), nullable=False)
    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), index=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    mobile_phone: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    whatsapp_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    contact_type: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    is_decision_maker: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    client: Mapped[Client] = relationship(back_populates="contacts")


class ClientActivity(Base):
    __tablename__ = "client_activities"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id"), index=True, nullable=False)
    activity_type: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    activity_title: Mapped[str] = mapped_column(String(200), nullable=False)
    activity_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_type: Mapped[str | None] = mapped_column(String(80), index=True, nullable=True)
    source_id: Mapped[uuid.UUID | None] = mapped_column(index=True, nullable=True)
    activity_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, index=True, nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    client: Mapped[Client] = relationship(back_populates="activities")
