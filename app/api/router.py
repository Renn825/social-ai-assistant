from fastapi import APIRouter, Depends

from app.api.routes import analysis, assistant, health, posts, reports, tasks
from app.auth import verify_api_key

api_router = APIRouter()
api_router.include_router(health.router)

protected_routers = [
    posts.router,
    tasks.router,
    analysis.router,
    reports.router,
    assistant.router,
]

for router in protected_routers:
    api_router.include_router(
        router,
        dependencies=[Depends(verify_api_key)],
    )
