from app.tools.logistics_tools import (
    fetch_shipments,
    warehouse_assignment,
    optimize_routes,
    delivery_eta,
    calculate_transport_cost,
    delivery_risk_analysis,
)

from app.schemas.recommendation import AgentRecommendation


class LogisticsAgent:
    def __init__(self, name: str = "LogisticsAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        # Step 1: Fetch shipment data
        shipments = fetch_shipments()

        # Step 2: Warehouse assignment
        warehouse = warehouse_assignment()

        # Step 3: Route optimization
        routes = optimize_routes()

        # Step 4: Delivery ETA
        eta = delivery_eta()

        # Step 5: Transportation cost
        transport_cost = calculate_transport_cost()

        # Step 6: Delivery risk analysis
        risk = delivery_risk_analysis()

        recommendation_text = (
            f"Processed {len(shipments)} shipment(s). "
            f"Recommended warehouse: {warehouse['recommended_warehouse']}. "
            f"Optimized delivery distance: {routes['total_distance_km']} km. "
            f"Estimated delivery time: {eta['estimated_delivery_hours']} hours "
            f"(Delay Probability: {eta['delay_probability'] * 100:.0f}%). "
            f"Average transport cost: ₹{transport_cost['average_transport_cost']:.2f}. "
            f"Delivery Risk: {risk['risk_level']} "
            f"(Score: {risk['risk_score']})."
        )

        confidence = 0.90

        metrics = {
            "shipments": shipments,
            "warehouse_assignment": warehouse,
            "routes": routes,
            "eta": eta,
            "transport_cost": transport_cost,
            "delivery_risk": risk,
        }

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=confidence,
            metrics=metrics,
        )


logistics_agent = LogisticsAgent()