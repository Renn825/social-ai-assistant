from fastapi import APIRouter

from app.api.routes import analysis, assistant, health, posts, reports, tasks

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(posts.router)
api_router.include_router(tasks.router)
api_router.include_router(analysis.router)
api_router.include_router(reports.router)
api_router.include_router(assistant.router)

