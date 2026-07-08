from fastapi import APIRouter, HTTPException

from app.db.session import check_database_connection

router = APIRouter(prefix="/db", tags=["database"])


@router.get("/health")
def database_health_check() -> dict[str, str]:
    try:
        check_database_connection()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        ) from exc

    return {
        "status": "ok",
        "service": "ResearchAI Database",
    }
