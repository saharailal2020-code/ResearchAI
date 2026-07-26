import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import inspect, text

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.session import engine
from app.models import Proposal


def add_missing_columns() -> None:
    inspector = inspect(engine)
    existing_columns = {column["name"] for column in inspector.get_columns("proposals")}

    with engine.begin() as connection:
        if "proposal_number" not in existing_columns:
            connection.execute(text("ALTER TABLE proposals ADD COLUMN proposal_number VARCHAR(50)"))
            print("Added proposals.proposal_number")

        if "proposal_owner_id" not in existing_columns:
            connection.execute(text("ALTER TABLE proposals ADD COLUMN proposal_owner_id UUID REFERENCES users(id)"))
            print("Added proposals.proposal_owner_id")


def backfill_existing_rows() -> None:
    with engine.begin() as connection:
        proposals = connection.execute(
            text("SELECT id, created_at, created_by, proposal_number FROM proposals ORDER BY created_at, id")
        ).mappings().all()

        sequence_by_date: dict[str, int] = {}
        for proposal in proposals:
            created_at = proposal["created_at"] or datetime.utcnow()
            date_key = created_at.strftime("%Y%m%d")
            sequence_by_date[date_key] = sequence_by_date.get(date_key, 0) + 1

            proposal_number = proposal["proposal_number"] or f"PROP-{date_key}-{sequence_by_date[date_key]:04d}"
            connection.execute(
                text(
                    """
                    UPDATE proposals
                    SET proposal_number = :proposal_number,
                        proposal_owner_id = COALESCE(proposal_owner_id, created_by)
                    WHERE id = :proposal_id
                    """
                ),
                {"proposal_number": proposal_number, "proposal_id": proposal["id"]},
            )


def create_missing_indexes() -> None:
    inspector = inspect(engine)
    existing_indexes = {index["name"] for index in inspector.get_indexes("proposals")}

    with engine.begin() as connection:
        if "ux_proposals_proposal_number" not in existing_indexes:
            connection.execute(
                text("CREATE UNIQUE INDEX ux_proposals_proposal_number ON proposals (proposal_number)")
            )
            print("Added unique index ux_proposals_proposal_number")

        if "ix_proposals_proposal_owner_id" not in existing_indexes:
            connection.execute(text("CREATE INDEX ix_proposals_proposal_owner_id ON proposals (proposal_owner_id)"))
            print("Added index ix_proposals_proposal_owner_id")


def main() -> None:
    Base.metadata.create_all(bind=engine, tables=[Proposal.__table__])
    add_missing_columns()
    backfill_existing_rows()
    create_missing_indexes()
    print("Proposal MVP backend upgrade is ready.")


if __name__ == "__main__":
    main()
