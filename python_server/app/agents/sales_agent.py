from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from tools.sales_tools import (
    fetch_sales_data,
    forecast_demand,
    calculate_growth,
    recommend_production
)

from core.adk_agent_runner import run_adk_agent


class SalesAgent:

    def __init__(self):

        self.name = "SalesAgent"

        self.agent = LlmAgent(

            name="sales_agent",

            model=LiteLlm(
                model="groq/llama-3.3-70b-versatile"
            ),

            instruction="""
You are a Sales Domain Agent.

You are responsible for analyzing sales,
demand forecasting, business growth, and
production requirements.

You have access to these tools:

1. fetch_sales_data
   - Fetch current sales data.

2. forecast_demand
   - Forecast future demand.

3. calculate_growth
   - Calculate sales growth.

4. recommend_production
   - Recommend production requirements.

Analyze the task assigned by the Planner Agent.

Use the available tools whenever necessary.

Consider:

- Current sales
- Demand forecast
- Forecast confidence
- Sales growth
- Production requirements

Return ONLY valid JSON:

{
    "agent_name": "SalesAgent",
    "recommendation": "Clear sales recommendation",
    "confidence": 0.90,
    "metrics": {
        "sales_data": {},
        "forecast": {},
        "growth": {},
        "production_recommendation": {}
    }
}

Do not invent data.

Use only information returned by the tools,
the assigned task, and provided parameters.
""",

            tools=[
                fetch_sales_data,
                forecast_demand,
                calculate_growth,
                recommend_production
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


sales_agent = SalesAgent()