from app.tools.inventory_tools import (
    fetch_inventory,
    demand_forecast,
    warehouse_capacity,
    reorder_recommendation,
    supplier_recommendation,
    inventory_risk_score,
    inventory_summary,
)
from app.schemas.recommendation import AgentRecommendation


class InventoryAgent:
    def __init__(self, name: str = "InventoryAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        # Step 1: Fetch inventory
        inventory = fetch_inventory()

        # Step 2: Forecast demand
        forecast = demand_forecast()

        # Step 3: Check warehouse capacity
        capacity = warehouse_capacity()

        # Step 4: Generate reorder recommendation
        reorder_rec = reorder_recommendation()

        # Step 5: Recommend supplier
        supplier = supplier_recommendation()

        # Step 6: Calculate inventory risk
        risk = inventory_risk_score()

        # Step 7: Generate inventory summary
        summary = inventory_summary()

        recommendation_text = summary["action"]

        confidence = 0.90

        metrics = {
            "inventory": inventory,
            "forecast": forecast,
            "capacity": capacity,
            "reorder_recommendation": reorder_rec,
            "supplier_recommendation": supplier,
            "inventory_risk": risk,
            "inventory_summary": summary,
        }

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=confidence,
            metrics=metrics,
        )


inventory_agent = InventoryAgent()