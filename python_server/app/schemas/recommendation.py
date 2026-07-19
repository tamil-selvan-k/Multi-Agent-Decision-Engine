from typing import Any, Dict
from pydantic import BaseModel

class AgentRecommendation(BaseModel):
    agent_name: str
    recommendation: str
    confidence: float
    metrics: Dict[str, Any]
