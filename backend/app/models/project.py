import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("proposal_id", name="uq_projects_proposal_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id"), index=True, nullable=False)
    proposal_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("proposals.id"), index=True, nullable=False)
    project_name: Mapped[str] = mapped_column(String(250), index=True, nullable=False)
    research_type: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    project_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    business_development_owner_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    project_manager_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Setup", index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    client: Mapped["Client"] = relationship(back_populates="projects")
    proposal: Mapped["Proposal"] = relationship(back_populates="project")
    business_development_owner: Mapped["User | None"] = relationship(foreign_keys=[business_development_owner_id])
    project_manager: Mapped["User | None"] = relationship(foreign_keys=[project_manager_id])
