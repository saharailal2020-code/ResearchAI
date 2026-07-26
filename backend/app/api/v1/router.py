from fastapi import APIRouter

from app.api.v1 import auth, clients, db, projects, proposals, questionnaires, sampling

router = APIRouter()


@router.get("/health", tags=["health"])
def api_health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "ResearchAI API",
        "version": "0.1.0",
    }


api_router = router
api_router.include_router(auth.router)
api_router.include_router(clients.router)
api_router.include_router(proposals.router)
api_router.include_router(projects.router)
api_router.include_router(questionnaires.router)
api_router.include_router(sampling.router)
api_router.include_router(db.router)
