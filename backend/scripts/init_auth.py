import sys
from pathlib import Path

from sqlalchemy import select

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import Role, User, UserRole

DEFAULT_ROLES = [
    "System Administrator",
    "Research Director",
    "Research Manager",
    "Project Manager",
    "Marketing",
    "Data Processing",
    "Data Analyst",
    "Quality Control",
]

ADMIN_EMAIL = "admin@researchai.local"
ADMIN_PASSWORD = "Admin123!"


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def seed_roles() -> None:
    with SessionLocal() as db:
        for role_name in DEFAULT_ROLES:
            existing_role = db.execute(
                select(Role).where(Role.role_name == role_name)
            ).scalar_one_or_none()
            if existing_role is None:
                db.add(Role(role_name=role_name, description=f"{role_name} role"))
        db.commit()


def seed_admin() -> None:
    with SessionLocal() as db:
        admin = db.execute(select(User).where(User.email == ADMIN_EMAIL)).scalar_one_or_none()
        if admin is None:
            admin = User(
                full_name="ResearchAI Admin",
                email=ADMIN_EMAIL,
                password_hash=hash_password(ADMIN_PASSWORD),
                status="active",
                is_active=True,
            )
            db.add(admin)
            db.flush()

        admin_role = db.execute(
            select(Role).where(Role.role_name == "System Administrator")
        ).scalar_one()
        existing_user_role = db.execute(
            select(UserRole).where(
                UserRole.user_id == admin.id,
                UserRole.role_id == admin_role.id,
            )
        ).scalar_one_or_none()
        if existing_user_role is None:
            db.add(UserRole(user_id=admin.id, role_id=admin_role.id))

        db.commit()


def main() -> None:
    create_tables()
    seed_roles()
    seed_admin()
    print("Authentication tables and default admin user are ready.")
    print(f"Admin email: {ADMIN_EMAIL}")
    print(f"Admin password: {ADMIN_PASSWORD}")


if __name__ == "__main__":
    main()
