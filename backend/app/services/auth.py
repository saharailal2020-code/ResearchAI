from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.security import verify_password
from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    statement = (
        select(User)
        .options(selectinload(User.user_roles))
        .where(User.email == email.lower().strip())
    )
    return db.execute(statement).scalar_one_or_none()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not user.is_active or user.status != "active":
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_user_roles(user: User) -> list[str]:
    return [user_role.role.role_name for user_role in user.user_roles if user_role.role.status == "active"]
