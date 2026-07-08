from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserProfile
from app.services.auth import authenticate_user, get_user_roles

router = APIRouter(prefix="/auth", tags=["auth"])


def build_user_profile(user: User) -> UserProfile:
    return UserProfile(
        id=str(user.id),
        full_name=user.full_name,
        email=user.email,
        roles=get_user_roles(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = authenticate_user(db, payload.email, payload.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user.last_login_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(subject=str(user.id))
    return TokenResponse(
        access_token=access_token,
        user=build_user_profile(user),
    )


@router.get("/me", response_model=UserProfile)
def get_me(current_user: User = Depends(get_current_user)) -> UserProfile:
    return build_user_profile(current_user)


@router.post("/logout")
def logout() -> dict[str, bool | str | None]:
    return {
        "success": True,
        "message": "Logout successful",
        "data": None,
    }
