from fastapi import APIRouter
from datetime import datetime
from app.schemas.decision import OrchestrationRequest
from app.core.adk_runner import run_adk_orchestration
from app.core.responses import ApiResponse
from app.core.logging import logger

router = APIRouter()

@router.post("/orchestrate")
async def trigger_agents(request: OrchestrationRequest):
    """
    Endpoint hit by the Node.js gateway to start a multi-agent negotiation.
    Runs domain agents, synthesizes decision, and returns full enterprise decision.
    """
    logger.info(f"Received orchestration trigger for session {request.session_id}")
    decision = run_adk_orchestration(request.session_id, request.parameters)

    return ApiResponse.success(
        data=decision.model_dump(),
        message="Multi-agent decision orchestration completed",
        status_code=200
    )

@router.get('/health')
async def health_check():
    return ApiResponse.success(
        data={
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
        },
        message="Orchestrator agent is running",
        status_code=200
    )