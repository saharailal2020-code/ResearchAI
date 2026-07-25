import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.session import engine
from app.models.proposal import Proposal


def main() -> None:
    Base.metadata.create_all(bind=engine, tables=[Proposal.__table__])
    print("Proposal management tables are ready.")


if __name__ == "__main__":
    main()
