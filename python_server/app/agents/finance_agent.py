from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from tools.finance_tools import (
    fetch_budget,
    anomaly_detection,
    cost_estimator,
    budget_impact
)

from core.adk_agent_runner import run_adk_agent


class FinanceAgent:

    def __init__(self):

        self.name = "FinanceAgent"

        self.agent = LlmAgent(
            name="finance_agent",

            model=LiteLlm(
                model="groq/llama-3.3-70b-versatile"
            ),

            instruction="""
You are a Finance Domain Agent.

You are responsible for analyzing financial
aspects of business decisions.

Analyze the task assigned by the Planner Agent.

Use the available tools when required:

- fetch_budget
- anomaly_detection
- cost_estimator
- budget_impact

Analyze the tool results and provide:

1. Financial situation
2. Key findings
3. Cost impact
4. Budget impact
5. Financial risks
6. Recommendation
7. Confidence

Do not invent data.
Use only the information available from
the tools, task, and parameters.
""",

            tools=[
                fetch_budget,
                anomaly_detection,
                cost_estimator,
                budget_impact
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


finance_agent = FinanceAgent()