from app.tools.finance_tools import (
    fetch_budget,
    anomaly_detection,
    cost_estimator,
    budget_impact,
    calculate_roi,
    financial_risk_score,
)

from app.schemas.recommendation import AgentRecommendation

class FinanceAgent:
    def __init__(self, name: str = "FinanceAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        # Step 1: Fetch budget
        budget_data = fetch_budget()

        # Step 2: Detect anomalies
        anomaly = anomaly_detection()

        # Step 3: Predict operational cost
        cost = cost_estimator()

        # Step 4: Calculate budget impact
        impact = budget_impact()

        # Step 5: Calculate ROI
        roi = calculate_roi()

        # Step 6: Calculate overall financial risk
        risk = financial_risk_score()

        # Build recommendation text
        recommendation_text = (
            f"Budget data: {budget_data}. "
            f"Anomaly detection: {anomaly}. "
            f"Predicted operational cost: {cost}. "
            f"Budget impact: {impact}. "
            f"ROI analysis: {roi}. "
            f"Financial risk assessment: {risk}."
        )

        # Confidence score
        confidence = 0.95

        if anomaly.get("anomaly", False):
            confidence -= 0.15

        if impact.get("budget_exceeded", False):
            confidence -= 0.10

        if risk.get("risk_level") == "High":
            confidence -= 0.10
        elif risk.get("risk_level") == "Medium":
            confidence -= 0.05

        confidence = max(0.50, round(confidence, 2))

        metrics = {
            "budget": budget_data,
            "anomaly": anomaly,
            "cost_prediction": cost,
            "budget_impact": impact,
            "roi": roi,
            "financial_risk": risk,
        }

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=confidence,
            metrics=metrics,
        )


finance_agent = FinanceAgent()