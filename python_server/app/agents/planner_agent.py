import json
import uuid
from typing import Dict, Any

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


class PlannerAgent:

    def __init__(self):

        self.name = "PlannerAgent"

        # ----------------------------------
        # ADK Planner Agent
        # ----------------------------------

        self.agent = LlmAgent(

            name="planner_agent",

            # Groq through LiteLLM
            model=LiteLlm(
                model="groq/llama-3.3-70b-versatile"
            ),

            instruction="""
You are the Planner Agent in an Enterprise
Multi-Agent Decision System.

Your responsibility is to analyze the user's
business request and create an execution plan.

You must determine:

1. Which domain agents need to be invoked.
2. What exact task should be assigned to each agent.
3. What parameters should be passed to each agent.

Available Agents:

InventoryAgent:
- Analyzes inventory levels.
- Analyzes warehouse capacity.
- Optimizes inventory.
- Determines reorder requirements.

LogisticsAgent:
- Analyzes shipments.
- Optimizes delivery routes.
- Calculates delivery ETA.
- Determines warehouse assignment.

SalesAgent:
- Analyzes sales data.
- Performs demand forecasting.
- Calculates growth.
- Recommends production levels.

FinanceAgent:
- Analyzes budgets.
- Detects financial anomalies.
- Estimates costs.
- Analyzes budget impact.

Planning Rules:

- Only select agents relevant to the user's request.
- If multiple domains are involved, select multiple agents.
- The task must be specific and actionable.
- Pass relevant information from the user request
  through the parameters.
- Do not invent parameters that are not provided.
- Do not perform the domain analysis yourself.
- Your job is ONLY to create the execution plan.

Return ONLY valid JSON.

Required format:

{
    "agents": [
        {
            "agent_name": "InventoryAgent",
            "task": "Analyze current inventory and determine reorder requirements.",
            "parameters": {}
        }
    ]
}
"""
        )

        # ----------------------------------
        # ADK Session Service
        # ----------------------------------

        self.session_service = (
            InMemorySessionService()
        )

        # ----------------------------------
        # ADK Runner
        # ----------------------------------

        self.runner = Runner(

            agent=self.agent,

            app_name="enterprise_orchestrator",

            session_service=self.session_service
        )

    async def plan(
        self,
        user_input: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:

        # ----------------------------------
        # Unique Session
        # ----------------------------------

        session_id = (
            f"planner-{uuid.uuid4().hex}"
        )

        # ----------------------------------
        # Create ADK Session
        # ----------------------------------

        await self.session_service.create_session(

            app_name="enterprise_orchestrator",

            user_id="orchestrator",

            session_id=session_id
        )

        # ----------------------------------
        # Build Planner Prompt
        # ----------------------------------

        prompt = f"""
USER REQUEST:

{user_input}


ADDITIONAL PARAMETERS:

{json.dumps(
    parameters,
    default=str,
    indent=2
)}


Create an execution plan for this request.

Determine:

1. Which agents should be invoked.
2. The exact task assigned to each agent.
3. The parameters passed to each agent.

Return ONLY valid JSON.
"""

        # ----------------------------------
        # ADK Message
        # ----------------------------------

        content = types.Content(

            role="user",

            parts=[
                types.Part(
                    text=prompt
                )
            ]
        )

        # ----------------------------------
        # Run Planner Agent
        # ----------------------------------

        final_text = None

        async for event in self.runner.run_async(

            user_id="orchestrator",

            session_id=session_id,

            new_message=content
        ):

            if event.is_final_response():

                if (
                    event.content
                    and event.content.parts
                ):

                    final_text = (
                        event.content.parts[0].text
                    )

        # ----------------------------------
        # Validate Response
        # ----------------------------------

        if not final_text:

            raise RuntimeError(
                "PlannerAgent did not return "
                "a final response"
            )

        final_text = final_text.strip()

        # ----------------------------------
        # Remove Markdown JSON Fences
        # ----------------------------------

        if final_text.startswith(
            "```json"
        ):

            final_text = final_text[
                len("```json"):
            ]

        elif final_text.startswith(
            "```"
        ):

            final_text = final_text[
                len("```"):
            ]

        if final_text.endswith(
            "```"
        ):

            final_text = final_text[
                :-len("```")
            ]

        final_text = final_text.strip()

        # ----------------------------------
        # Parse JSON
        # ----------------------------------

        try:

            plan = json.loads(
                final_text
            )

        except json.JSONDecodeError as e:

            raise RuntimeError(
                f"PlannerAgent returned "
                f"invalid JSON: {final_text}"
            ) from e

        # ----------------------------------
        # Validate Plan Structure
        # ----------------------------------

        if not isinstance(
            plan,
            dict
        ):

            raise RuntimeError(
                "PlannerAgent response "
                "must be a JSON object"
            )

        if "agents" not in plan:

            raise RuntimeError(
                "PlannerAgent response "
                "does not contain 'agents'"
            )

        return plan