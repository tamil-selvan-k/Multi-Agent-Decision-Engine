from app.tools.finance_tools import assess_budget_constraints
from app.schemas.recommendation import AgentRecommendation

class FinanceAgent:
    def __init__(self, name: str = "FinanceAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        metrics = assess_budget_constraints()
        recommendation_text = (
            f"Approve promotional expenditure within available budget cap of ${metrics['available_budget']} {metrics['currency']}."
        )
        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=metrics.get("confidence", 0.95),
            metrics=metrics,
        )

finance_agent = FinanceAgent()
