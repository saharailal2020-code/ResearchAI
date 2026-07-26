import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Questionnaire(Base):
    __tablename__ = "questionnaires"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), index=True, nullable=False)
    questionnaire_name: Mapped[str] = mapped_column(String(250), index=True, nullable=False)
    target_respondent: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    instrument_type: Mapped[str] = mapped_column(String(100), default="Quantitative Survey", index=True, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="Draft", index=True, nullable=False)
    kobo_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    xlsform_link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    project: Mapped["Project"] = relationship(back_populates="questionnaires")
    sample_groups: Mapped[list["SampleGroup"]] = relationship(back_populates="questionnaire")
