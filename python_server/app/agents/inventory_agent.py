from app.tools.inventory_tools import fetch_inventory, optimize_inventory, warehouse_capacity, reorder_recommendation
from app.schemas.recommendation import AgentRecommendation

class InventoryAgent:
    def __init__(self, name: str = "InventoryAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        # Step 1: Fetch inventory
        inventory = fetch_inventory()
        # Step 2: Optimize inventory
        optimization = optimize_inventory()
        # Step 3: Check warehouse capacity
        capacity = warehouse_capacity()
        # Step 4: Get reorder recommendation
        reorder_rec = reorder_recommendation()

        # Build recommendation text
        recommendation_text = (
            f"Current stock: {inventory['current_stock']} units, "
            f"warehouse capacity: {inventory['warehouse_capacity']} units, "
            f"utilization: {capacity['utilization']}%, "
            f"recommended stock: {optimization['recommended_stock']} units, "
            f"action: {reorder_rec}"
        )

        # Confidence could be based on data quality; we'll use a fixed high confidence
        confidence = 0.89

        metrics = {
            "inventory": inventory,
            "optimization": optimization,
            "capacity": capacity,
            "reorder_recommendation": reorder_rec
        }

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=confidence,
            metrics=metrics,
        )

inventory_agent = InventoryAgent()