import logging
from typing import Dict, Any, Optional

from agents.planner_agent import PlannerAgent
from agents.sales_agent import sales_agent
from agents.inventory_agent import inventory_agent
from agents.finance_agent import finance_agent
from agents.logistics_agent import logistics_agent

from core.decision_engine import generate_decision
from schemas.decision import EnterpriseDecision


logger = logging.getLogger(__name__)


# Create Planner once
planner_agent = PlannerAgent()


# Registry of available domain agents
AGENT_REGISTRY = {
    "SalesAgent": sales_agent,
    "InventoryAgent": inventory_agent,
    "FinanceAgent": finance_agent,
    "LogisticsAgent": logistics_agent,
}


async def run_adk_orchestration(
    session_id: str,
    user_input: str,
    parameters: Dict[str, Any]
) -> EnterpriseDecision:

    logger.info(
        f"Starting orchestration for: {user_input}"
    )

    # 1. Planner decides which agents to invoke
    plan = await planner_agent.plan(
        user_input=user_input,
        parameters=parameters
    )

    # 2. Execute selected agents
    agent_outputs = []

    for agent_plan in plan.get("agents", []):

        agent_name = agent_plan.get("agent_name")
        task = agent_plan.get("task", "")

        agent_parameters = agent_plan.get(
            "parameters",
            {}
        )

        agent = AGENT_REGISTRY.get(
            agent_name
        )

        if not agent:
            logger.warning(
                f"Agent not found: {agent_name}"
            )
            continue

        logger.info(
            f"Running {agent_name}"
        )

        result = await agent.run(
            task=task,
            parameters={
                **parameters,
                **agent_parameters
            }
        )

        agent_outputs.append(result)

    # 3. Synthesis
    final_decision = await synthesis_agent.synthesize(
        user_input=user_input,
        agent_results=agent_outputs
    )

    return EnterpriseDecision(
        session_id=session_id,
        user_input=user_input,
        plan=plan,
        agent_results=agent_outputs,
        final_decision=final_decision
    )