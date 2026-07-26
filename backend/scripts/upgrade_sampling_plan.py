import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.base import Base
from app.db.session import engine
from app.models import SampleGroup, SamplingTarget


def main() -> None:
    Base.metadata.create_all(bind=engine, tables=[SampleGroup.__table__, SamplingTarget.__table__])
    print("Sampling Plan tables are ready.")


if __name__ == "__main__":
    main()
