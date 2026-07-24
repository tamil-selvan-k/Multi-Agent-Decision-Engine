import json
import uuid
from typing import Any, Dict

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from schemas.recommendation import AgentRecommendation


async def run_adk_agent(
    agent,
    agent_name: str,
    task: str,
    parameters: Dict[str, Any]
) -> AgentRecommendation:

    # ---------------------------------
    # Create ADK session service
    # ---------------------------------

    session_service = InMemorySessionService()

    # ---------------------------------
    # Create ADK Runner
    # ---------------------------------

    runner = Runner(
        agent=agent,
        app_name="enterprise_orchestrator",
        session_service=session_service
    )

    # Unique session per agent execution
    session_id = (
        f"{agent_name.lower()}-"
        f"{uuid.uuid4().hex}"
    )

    # ---------------------------------
    # Create ADK Session
    # ---------------------------------

    await session_service.create_session(
        app_name="enterprise_orchestrator",
        user_id="orchestrator",
        session_id=session_id
    )

    # ---------------------------------
    # Build Prompt
    # ---------------------------------

    prompt = f"""
You are the {agent_name}.

You are executing a specific task assigned
by the Planner Agent.

TASK:
{task}

PARAMETERS:
{json.dumps(parameters, default=str)}

Execute the task using your available tools.

Analyze the tool results carefully.

Return ONLY valid JSON in this exact format:

{{
    "agent_name": "{agent_name}",
    "recommendation": "Your recommendation",
    "confidence": 0.0,
    "metrics": {{}}
}}

Rules:

- Do not invent data.
- Use the available tools when necessary.
- Base your recommendation on actual tool results.
- Confidence must be a number between 0.0 and 1.0.
"""

    # ---------------------------------
    # Create ADK Message
    # ---------------------------------

    content = types.Content(
        role="user",
        parts=[
            types.Part(
                text=prompt
            )
        ]
    )

    # ---------------------------------
    # Run ADK Agent
    # ---------------------------------

    final_text = None

    async for event in runner.run_async(
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

    # ---------------------------------
    # Validate Response
    # ---------------------------------

    if not final_text:

        raise RuntimeError(
            f"{agent_name} did not return "
            f"a response"
        )

    final_text = final_text.strip()

    # ---------------------------------
    # Remove Markdown JSON
    # ---------------------------------

    if final_text.startswith("```json"):

        final_text = final_text[
            len("```json"):
        ]

    elif final_text.startswith("```"):

        final_text = final_text[
            len("```"):
        ]

    if final_text.endswith("```"):

        final_text = final_text[
            :-len("```")
        ]

    final_text = final_text.strip()

    # ---------------------------------
    # Parse JSON
    # ---------------------------------

    try:

        result = json.loads(
            final_text
        )

    except json.JSONDecodeError as e:

        raise RuntimeError(
            f"{agent_name} returned invalid JSON: "
            f"{final_text}"
        ) from e

    # ---------------------------------
    # Return Standard Agent Result
    # ---------------------------------

    return AgentRecommendation(

        agent_name=result.get(
            "agent_name",
            agent_name
        ),

        recommendation=result.get(
            "recommendation",
            ""
        ),

        confidence=float(
            result.get(
                "confidence",
                0.0
            )
        ),

        metrics=result.get(
            "metrics",
            {}
        )
    )