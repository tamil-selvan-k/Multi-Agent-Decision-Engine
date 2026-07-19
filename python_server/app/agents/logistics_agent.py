from app.tools.logistics_tools import evaluate_shipping_capacity
from app.schemas.recommendation import AgentRecommendation

class LogisticsAgent:
    def __init__(self, name: str = "LogisticsAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        metrics = evaluate_shipping_capacity()
        recommendation_text = (
            f"Carrier freight capacity is at {metrics['carrier_capacity_percent']}% with {metrics['avg_lead_days']} days average lead time."
        )
        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=metrics.get("confidence", 0.90),
            metrics=metrics,
        )

logistics_agent = LogisticsAgent()
