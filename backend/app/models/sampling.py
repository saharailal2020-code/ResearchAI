import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SampleGroup(Base):
    __tablename__ = "sample_groups"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), index=True, nullable=False)
    questionnaire_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("questionnaires.id"),
        index=True,
        nullable=True,
    )
    sample_group_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    target_respondent: Mapped[str | None] = mapped_column(String(150), index=True, nullable=True)
    total_target_sample: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="Draft", index=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    project: Mapped["Project"] = relationship(back_populates="sample_groups")
    questionnaire: Mapped["Questionnaire | None"] = relationship(back_populates="sample_groups")
    targets: Mapped[list["SamplingTarget"]] = relationship(
        back_populates="sample_group",
        cascade="all, delete-orphan",
        order_by="SamplingTarget.sort_order",
    )


class SamplingTarget(Base):
    __tablename__ = "sampling_targets"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    sample_group_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sample_groups.id"), index=True, nullable=False)
    region_type: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    region_name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    target_sample: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    sample_group: Mapped[SampleGroup] = relationship(back_populates="targets")
