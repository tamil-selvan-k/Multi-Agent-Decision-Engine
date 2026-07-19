from app.tools.sales_tools import forecast_sales
from app.schemas.recommendation import AgentRecommendation

class SalesAgent:
    def __init__(self, name: str = "SalesAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        metrics = forecast_sales()
        recommendation_text = (
            f"Capitalize on Q3 demand growth with target sales forecast of {metrics['forecast']} units."
        )
        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=metrics.get("confidence", 0.90),
            metrics=metrics,
        )

sales_agent = SalesAgent()
