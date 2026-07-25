import sys
from pathlib import Path

from sqlalchemy import inspect, text

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.session import engine
from app.models import Client, ClientActivity, ClientContact


CLIENT_COLUMNS = {
    "logo_url": "VARCHAR(500)",
    "address": "TEXT",
    "city": "VARCHAR(100)",
    "province": "VARCHAR(100)",
    "country": "VARCHAR(100)",
    "website": "VARCHAR(250)",
    "last_activity_at": "TIMESTAMP WITH TIME ZONE",
    "next_follow_up_at": "TIMESTAMP WITH TIME ZONE",
    "customer_since": "TIMESTAMP WITH TIME ZONE",
}

CLIENT_CONTACT_COLUMNS = {
    "mobile_phone": "VARCHAR(50)",
    "whatsapp_number": "VARCHAR(50)",
    "contact_type": "VARCHAR(50)",
    "is_decision_maker": "BOOLEAN NOT NULL DEFAULT false",
}

INDEXES = [
    ("ix_clients_city", "clients", "city"),
    ("ix_clients_last_activity_at", "clients", "last_activity_at"),
    ("ix_clients_next_follow_up_at", "clients", "next_follow_up_at"),
    ("ix_client_contacts_mobile_phone", "client_contacts", "mobile_phone"),
    ("ix_client_contacts_contact_type", "client_contacts", "contact_type"),
]


def add_missing_columns(table_name: str, column_definitions: dict[str, str]) -> None:
    inspector = inspect(engine)
    existing_columns = {column["name"] for column in inspector.get_columns(table_name)}

    with engine.begin() as connection:
        for column_name, column_type in column_definitions.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"))
                print(f"Added {table_name}.{column_name}")


def create_missing_indexes() -> None:
    inspector = inspect(engine)

    with engine.begin() as connection:
        for index_name, table_name, column_name in INDEXES:
            existing_indexes = {index["name"] for index in inspector.get_indexes(table_name)}
            if index_name not in existing_indexes:
                connection.execute(text(f"CREATE INDEX {index_name} ON {table_name} ({column_name})"))
                print(f"Added index {index_name}")


def main() -> None:
    Base.metadata.create_all(bind=engine, tables=[Client.__table__, ClientContact.__table__, ClientActivity.__table__])
    add_missing_columns("clients", CLIENT_COLUMNS)
    add_missing_columns("client_contacts", CLIENT_CONTACT_COLUMNS)
    create_missing_indexes()
    print("Client Management v0.2 database upgrade is ready.")


if __name__ == "__main__":
    main()
