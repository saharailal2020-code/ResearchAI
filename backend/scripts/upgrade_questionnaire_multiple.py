import sys
from pathlib import Path

from sqlalchemy import inspect, text

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.session import engine
from app.models import Questionnaire


QUESTIONNAIRE_COLUMNS = {
    "target_respondent": "VARCHAR(150)",
    "instrument_type": "VARCHAR(100)",
    "sort_order": "INTEGER",
}


def add_missing_columns() -> None:
    inspector = inspect(engine)
    existing_columns = {column["name"] for column in inspector.get_columns("questionnaires")}

    with engine.begin() as connection:
        for column_name, column_type in QUESTIONNAIRE_COLUMNS.items():
            if column_name not in existing_columns:
                connection.execute(
                    text(f"ALTER TABLE questionnaires ADD COLUMN {column_name} {column_type}")
                )
                print(f"Added questionnaires.{column_name}")


def backfill_existing_rows() -> None:
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                UPDATE questionnaires
                SET target_respondent = COALESCE(NULLIF(target_respondent, ''), 'Main Respondent'),
                    instrument_type = COALESCE(NULLIF(instrument_type, ''), 'Quantitative Survey')
                """
            )
        )
        connection.execute(
            text(
                """
                WITH ordered_questionnaires AS (
                    SELECT
                        id,
                        ROW_NUMBER() OVER (PARTITION BY project_id ORDER BY created_at, id) AS row_number
                    FROM questionnaires
                )
                UPDATE questionnaires
                SET sort_order = ordered_questionnaires.row_number
                FROM ordered_questionnaires
                WHERE questionnaires.id = ordered_questionnaires.id
                  AND questionnaires.sort_order IS NULL
                """
            )
        )


def relax_one_questionnaire_constraint() -> None:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE questionnaires DROP CONSTRAINT IF EXISTS uq_questionnaires_project_id"))


def enforce_required_columns() -> None:
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE questionnaires ALTER COLUMN target_respondent SET NOT NULL"))
        connection.execute(text("ALTER TABLE questionnaires ALTER COLUMN instrument_type SET NOT NULL"))
        connection.execute(text("ALTER TABLE questionnaires ALTER COLUMN sort_order SET NOT NULL"))


def main() -> None:
    Base.metadata.create_all(bind=engine, tables=[Questionnaire.__table__])
    add_missing_columns()
    backfill_existing_rows()
    relax_one_questionnaire_constraint()
    enforce_required_columns()
    print("Questionnaire multiple-instrument database upgrade is ready.")


if __name__ == "__main__":
    main()
