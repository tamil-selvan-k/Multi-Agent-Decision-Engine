from app.tools.inventory_tools import check_inventory_levels
from app.schemas.recommendation import AgentRecommendation

class InventoryAgent:
    def __init__(self, name: str = "InventoryAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        metrics = check_inventory_levels()
        recommendation_text = (
            f"Maintain safety buffer. Current stock level is {metrics['stock_level']} units with low stockout risk."
        )
        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=metrics.get("confidence", 0.89),
            metrics=metrics,
        )

inventory_agent = InventoryAgent()
