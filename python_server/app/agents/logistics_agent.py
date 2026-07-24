from typing import Dict, Any

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from tools.logistics_tools import (
    fetch_shipments,
    optimize_routes,
    delivery_eta,
    warehouse_assignment
)

from core.adk_agent_runner import run_adk_agent


class LogisticsAgent:

    def __init__(self):

        self.name = "LogisticsAgent"

        self.agent = LlmAgent(

            name="logistics_agent",

            # Groq through LiteLLM
            model=LiteLlm(
                model="groq/llama-3.3-70b-versatile"
            ),

            instruction="""
You are a Logistics Domain Agent.

Your responsibility is to analyze logistics
and supply-chain related business problems.

You have access to the following tools:

1. fetch_shipments
   - Fetch active shipments.

2. optimize_routes
   - Find the best delivery route.

3. delivery_eta
   - Calculate delivery ETA and delay probability.

4. warehouse_assignment
   - Determine the best warehouse assignment.

You should decide which tools are necessary
to complete the assigned task.

Analyze the tool results carefully.

Consider:

- Active shipments
- Best delivery route
- Route distance
- Delivery ETA
- Delay probability
- Warehouse assignment

Return ONLY valid JSON:

{
    "agent_name": "LogisticsAgent",
    "recommendation": "Clear logistics recommendation",
    "confidence": 0.90,
    "metrics": {
        "shipments": {},
        "routes": {},
        "eta": {},
        "warehouse_assignment": {}
    }
}

Do not invent data.
Use only information returned by the tools,
the assigned task, and provided parameters.
""",

            tools=[
                fetch_shipments,
                optimize_routes,
                delivery_eta,
                warehouse_assignment
            ]
        )

    async def run(
        self,
        task: str,
        parameters: Dict[str, Any]
    ):

        return await run_adk_agent(

            agent=self.agent,

            agent_name=self.name,

            task=task,

            parameters=parameters
        )


logistics_agent = LogisticsAgent()