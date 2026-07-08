from fastapi import APIRouter

from app.api.v1 import db

router = APIRouter()


@router.get("/health", tags=["health"])
def api_health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ResearchAI API",
        "version": "0.1.0",
    }


api_router = router
api_router.include_router(db.router)
