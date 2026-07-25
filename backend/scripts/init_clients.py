import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.session import engine
from app.models import Client, ClientActivity, ClientContact


def main() -> None:
    Base.metadata.create_all(bind=engine, tables=[Client.__table__, ClientContact.__table__, ClientActivity.__table__])
    print("Client management tables are ready.")


if __name__ == "__main__":
    main()
