from app.tools.finance_tools import fetch_budget, anomaly_detection, cost_estimator, budget_impact
from app.schemas.recommendation import AgentRecommendation

class FinanceAgent:
    def __init__(self, name: str = "FinanceAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        # Step 1: Fetch budget
        budget_data = fetch_budget()
        # Step 2: Anomaly detection
        anomaly = anomaly_detection()
        # Step 3: Cost estimation
        cost = cost_estimator()
        # Step 4: Budget impact
        impact = budget_impact()

        # Build recommendation text
        recommendation_text = (
            f"Budget data: {budget_data}, "
            f"Anomaly detection: {anomaly}, "
            f"Cost estimate: {cost}, "
            f"Budget impact: {impact}"
        )

        # Confidence could be based on anomaly score etc.
        confidence = 0.95 if not anomaly.get("anomaly", True) else 0.70

        metrics = {
            "budget": budget_data,
            "anomaly": anomaly,
            "cost_estimate": cost,
            "budget_impact": impact
        }

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=confidence,
            metrics=metrics,
        )

finance_agent = FinanceAgent()