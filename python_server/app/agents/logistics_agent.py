from app.tools.logistics_tools import fetch_shipments, optimize_routes, delivery_eta, warehouse_assignment
from app.schemas.recommendation import AgentRecommendation

class LogisticsAgent:
    def __init__(self, name: str = "LogisticsAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        # Step 1: Fetch shipments
        shipments = fetch_shipments()
        # Step 2: Optimize routes
        routes = optimize_routes()
        # Step 3: Delivery ETA
        eta = delivery_eta()
        # Step 4: Warehouse assignment
        warehouse = warehouse_assignment()

        # Build recommendation text
        recommendation_text = (
            f"Active shipments: {len(shipments)} items, "
            f"optimized route: {routes['best_route']} (distance: {routes['total_distance_km']} km), "
            f"ETA: {eta['estimated_delivery_hours']} hours with {eta['delay_probability']*100:.0f}% delay probability, "
            f"recommended warehouse: {warehouse['recommended_warehouse']}"
        )

        # Confidence could be based on route optimization quality etc.
        confidence = 0.90

        metrics = {
            "shipments": shipments,
            "routes": routes,
            "eta": eta,
            "warehouse_assignment": warehouse
        }

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=confidence,
            metrics=metrics,
        )

logistics_agent = LogisticsAgent()