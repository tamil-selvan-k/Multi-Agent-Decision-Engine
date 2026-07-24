from fastapi import APIRouter
from datetime import datetime

from schemas.decision import OrchestrationRequest
from core.adk_runner import run_adk_orchestration
from core.responses import ApiResponse
from core.logging import logger

router = APIRouter()


@router.post("/orchestrate")
async def trigger_agents(request: OrchestrationRequest):

    logger.info(
        f"Received orchestration trigger "
        f"for session {request.session_id}"
    )

    decision = await run_adk_orchestration(
        session_id=request.session_id,
        user_input=request.user_input,
        parameters=request.parameters
    )

    return ApiResponse.success(
        data=decision.model_dump(),
        message="Multi-agent decision orchestration completed",
        status_code=200
    )

@router.get("/health")
async def health_check():

    return ApiResponse.success(
        data={
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
        },
        message="Orchestrator agent is running",
        status_code=200
    )