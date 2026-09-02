from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.agents.assistant import AssistantAgent
from app.core.database import get_session
from app.schemas.assistant import AssistantRequest, AssistantResponse

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/chat", response_model=AssistantResponse)
def chat(
    request: AssistantRequest,
    session: Session = Depends(get_session),
) -> AssistantResponse:
    agent = AssistantAgent(session)
    result = agent.run(request.message)
    return AssistantResponse(**result)

