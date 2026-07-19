import logging
from typing import Dict, Any, Optional
from app.agents.sales_agent import sales_agent
from app.agents.inventory_agent import inventory_agent
from app.agents.finance_agent import finance_agent
from app.agents.logistics_agent import logistics_agent
from app.core.decision_engine import generate_decision
from app.schemas.decision import EnterpriseDecision

logger = logging.getLogger(__name__)

def run_adk_orchestration(session_id: str, parameters: Optional[Dict[str, Any]] = None) -> EnterpriseDecision:
    """
    Google ADK Orchestrator:
    Runs domain agents (Sales, Inventory, Finance, Logistics), collects output recommendations,
    and invokes the enterprise decision engine.
    """
    logger.info(f"[ADK Orchestrator] Running negotiation for session '{session_id}'")

    # Run domain specialist agents
    sales_output = sales_agent.run()
    inventory_output = inventory_agent.run()
    finance_output = finance_agent.run()
    logistics_output = logistics_agent.run()

    agent_outputs = [sales_output, inventory_output, finance_output, logistics_output]

    # Synthesize outputs into final decision
    decision = generate_decision(session_id, agent_outputs)
    logger.info(f"[ADK Orchestrator] Completed negotiation for session '{session_id}'")
    return decision
