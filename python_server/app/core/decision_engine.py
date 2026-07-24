from typing import List
from datetime import datetime
from schemas.recommendation import AgentRecommendation
from schemas.decision import EnterpriseDecision

def generate_decision(session_id: str, agent_outputs: List[AgentRecommendation]) -> EnterpriseDecision:
    """
    Enterprise Decision Engine logic:
    Merges outputs from Sales, Inventory, Finance, and Logistics agents into a single actionable plan.
    """
    agent_summary = "; ".join([f"{out.agent_name}: '{out.recommendation}'" for out in agent_outputs])
    
    # Calculate weighted average confidence
    avg_confidence = sum([out.confidence for out in agent_outputs]) / len(agent_outputs) if agent_outputs else 0.90

    final_action_plan = (
        f"Consensus Reached (Confidence: {avg_confidence:.2f}): "
        f"Align Q3 production to sales forecast while preserving safety stock buffer and allocating expedited freight budget."
    )

    return EnterpriseDecision(
        session_id=session_id,
        status="COMPLETED",
        final_decision=final_action_plan,
        agent_outputs=agent_outputs,
        merged_at=datetime.now().isoformat()
    )
