from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from schemas.recommendation import AgentRecommendation
from typing import Any, Dict
from pydantic import BaseModel, Field


class OrchestrationRequest(BaseModel):

    session_id: str = Field(
        ...,
        description="Unique session ID"
    )

    user_input: str = Field(
        ...,
        description="Business request to analyze"
    )

    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional scenario parameters"
    )
    
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
