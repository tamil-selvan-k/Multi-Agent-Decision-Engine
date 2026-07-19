from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.schemas.recommendation import AgentRecommendation

class OrchestrationRequest(BaseModel):
    session_id: str = Field(..., description="Unique session ID for the negotiation process")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Scenario metrics and variables")

class EnterpriseDecision(BaseModel):
    session_id: str
    status: str
    final_decision: str
    agent_outputs: List[AgentRecommendation]
    merged_at: str

class OrchestrationResponse(BaseModel):
    session_id: str
    status: str
    message: str
    result: Optional[EnterpriseDecision] = None
