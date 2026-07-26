import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    proposal_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id"), index=True, nullable=False)
    proposal_owner_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    proposal_title: Mapped[str] = mapped_column(String(250), index=True, nullable=False)
    research_type: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    research_objective: Mapped[str | None] = mapped_column(Text, nullable=True)
    methodology_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_timeline: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estimated_budget: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Draft", index=True, nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    client: Mapped["Client"] = relationship(back_populates="proposals")
    proposal_owner: Mapped["User | None"] = relationship(foreign_keys=[proposal_owner_id])
