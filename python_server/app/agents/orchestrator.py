from app.agents.registry import AGENT_REGISTRY
from app.agents.planner_agent import PlannerAgent
from app.agents.synthesis_agent import SynthesisAgent


class Orchestrator:

    def __init__(self):

        self.planner = PlannerAgent()

        self.synthesis = SynthesisAgent()

    async def run(
        self,
        user_input: str,
        parameters: dict
    ):

        # --------------------------------
        # STEP 1: Planner Agent
        # --------------------------------

        plan = await self.planner.plan(
            user_input=user_input,
            parameters=parameters
        )

        print("\n========== PLANNER PLAN ==========")
        print(plan)

        # --------------------------------
        # STEP 2: Execute Selected Agents
        # --------------------------------

        agent_results = []

        for agent_plan in plan.get(
            "agents",
            []
        ):

            agent_name = agent_plan.get(
                "agent_name"
            )

            task = agent_plan.get(
                "task",
                ""
            )

            agent_parameters = agent_plan.get(
                "parameters",
                {}
            )

            print(
                f"\nExecuting Agent: "
                f"{agent_name}"
            )

            print(
                f"Assigned Task: "
                f"{task}"
            )

            print(
                f"Parameters: "
                f"{agent_parameters}"
            )

            # --------------------------------
            # Get Agent From Registry
            # --------------------------------

            agent = AGENT_REGISTRY.get(
                agent_name
            )

            if not agent:

                print(
                    f"Agent not found: "
                    f"{agent_name}"
                )

                continue

            try:

                # --------------------------------
                # Execute ADK Agent
                # --------------------------------

                result = await agent.run(

                    task=task,

                    parameters=agent_parameters
                )

                agent_results.append(
                    result
                )

                print(
                    f"{agent_name} completed successfully"
                )

            except Exception as e:

                print(
                    f"{agent_name} failed: {str(e)}"
                )

        # --------------------------------
        # STEP 3: Synthesis Agent
        # --------------------------------

        print(
            "\n========== SYNTHESIS =========="
        )

        final_decision = (
            await self.synthesis.synthesize(

                user_input=user_input,

                agent_results=agent_results
            )
        )

        # --------------------------------
        # STEP 4: Return Final Response
        # --------------------------------

        return {

            "plan": plan,

            "agent_results": [

                {
                    "agent_name":
                        result.agent_name,

                    "recommendation":
                        result.recommendation,

                    "confidence":
                        result.confidence,

                    "metrics":
                        result.metrics

                }

                for result in agent_results
            ],

            "final_decision":
                final_decision
        }