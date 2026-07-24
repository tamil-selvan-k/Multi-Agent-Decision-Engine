from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from tools.inventory_tools import (
    fetch_inventory,
    optimize_inventory,
    warehouse_capacity,
    reorder_recommendation
)

from core.adk_agent_runner import run_adk_agent


class InventoryAgent:

    def __init__(self):

        self.name = "InventoryAgent"

        self.agent = LlmAgent(

            name="inventory_agent",

            model=LiteLlm(
                model="groq/llama-3.3-70b-versatile"
            ),

            instruction="""
You are an Inventory Domain Agent.

You are responsible for analyzing inventory
and warehouse-related business problems.

You have access to these tools:

1. fetch_inventory
   - Fetch current inventory levels
   - Fetch warehouse capacity information

2. optimize_inventory
   - Determine optimal inventory levels

3. warehouse_capacity
   - Analyze warehouse utilization

4. reorder_recommendation
   - Determine whether inventory should be reordered

Analyze the task assigned by the Planner Agent.

Use the available tools whenever necessary.

Consider:

- Current stock
- Warehouse capacity
- Warehouse utilization
- Recommended stock level
- Reorder requirements

Return ONLY valid JSON:

{
    "agent_name": "InventoryAgent",
    "recommendation": "Clear inventory recommendation",
    "confidence": 0.90,
    "metrics": {
        "inventory": {},
        "optimization": {},
        "capacity": {},
        "reorder_recommendation": {}
    }
}

Do not invent data.
Use only information returned by the tools,
the assigned task, and provided parameters.
""",

            tools=[
                fetch_inventory,
                optimize_inventory,
                warehouse_capacity,
                reorder_recommendation
            ]
        )

    async def run(
        self,
        task: str,
        parameters: dict
    ):

        return await run_adk_agent(
            agent=self.agent,
            agent_name=self.name,
            task=task,
            parameters=parameters
        )


inventory_agent = InventoryAgent()