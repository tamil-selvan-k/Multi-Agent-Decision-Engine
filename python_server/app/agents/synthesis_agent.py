import uuid
import json

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


class SynthesisAgent:

    def __init__(self):

        self.name = "SynthesisAgent"

        # ----------------------------------
        # ADK Synthesis Agent
        # ----------------------------------

        self.agent = LlmAgent(

            name="synthesis_agent",

            # Groq through LiteLLM
            model=LiteLlm(
                model="groq/llama-3.3-70b-versatile"
            ),

            instruction="""
You are a Decision Synthesis Agent in an
Enterprise Multi-Agent Decision System.

You receive:

1. The original user request.
2. Recommendations from multiple domain-specific
   business agents.

Your responsibility is to analyze all agent results
and produce one final enterprise-level decision.

Your response MUST include:

1. Overall Situation
2. Key Findings
3. Agent Recommendations
4. Conflicting Recommendations
5. Recommended Action
6. Risks
7. Overall Confidence

Rules:

- Consider all available agent results.
- Identify conflicts between agents.
- Give priority to relevant and high-confidence findings.
- Do not invent facts.
- Use only the user request and agent results.
- Clearly explain the final recommended action.

Return ONLY valid JSON:

{
    "overall_situation": "",
    "key_findings": [],
    "agent_recommendations": [],
    "conflicting_recommendations": [],
    "recommended_action": "",
    "risks": [],
    "overall_confidence": 0.0
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

    async def synthesize(
        self,
        user_input: str,
        agent_results: list
    ):

        # ----------------------------------
        # Create Results Text
        # ----------------------------------

        results_text = "\n\n".join(

            [
                f"""
Agent Name:
{result.agent_name}

Recommendation:
{result.recommendation}

Confidence:
{result.confidence}

Metrics:
{json.dumps(
    result.metrics,
    default=str,
    indent=2
)}
"""
                for result in agent_results
            ]
        )

        # ----------------------------------
        # Create Prompt
        # ----------------------------------

        prompt = f"""
USER REQUEST:

{user_input}


DOMAIN AGENT RESULTS:

{results_text}


Analyze all domain agent results.

Synthesize them into one final enterprise
business decision.

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
        # Run Synthesis Agent
        # ----------------------------------

        final_text = None

        session_id = (
            f"synthesis-{uuid.uuid4().hex}"
        )

        await self.session_service.create_session(

            app_name="enterprise_orchestrator",

            user_id="orchestrator",

            session_id=session_id
        )

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
                "SynthesisAgent did not return "
                "a final response"
            )

        final_text = final_text.strip()

        # ----------------------------------
        # Remove Markdown JSON
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
                :-len("```"):
            ]

        final_text = final_text.strip()

        # ----------------------------------
        # Parse JSON
        # ----------------------------------

        try:

            return json.loads(
                final_text
            )

        except json.JSONDecodeError as e:

            raise RuntimeError(
                f"SynthesisAgent returned "
                f"invalid JSON: {final_text}"
            ) from e