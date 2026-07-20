from app.tools.sales_tools import fetch_sales_data, forecast_demand, calculate_growth, recommend_production
from app.schemas.recommendation import AgentRecommendation

class SalesAgent:
    def __init__(self, name: str = "SalesAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        # Step 1: Fetch sales data
        sales_data = fetch_sales_data()
        # Step 2: Forecast demand
        forecast = forecast_demand()
        # Step 3: Calculate growth
        growth = calculate_growth()
        # Step 4: Get production recommendation
        production_rec = recommend_production()

        # Build recommendation text
        recommendation_text = (
            f"Based on sales data {sales_data}, forecast demand of {forecast['forecast']} units "
            f"with {forecast['confidence']*100:.0f}% confidence, growth of {growth['growth']}%, "
            f"recommendation: {production_rec}"
        )

        # Combine metrics
        metrics = {
            "sales_data": sales_data,
            "forecast": forecast,
            "growth": growth,
            "production_recommendation": production_rec
        }

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation_text,
            confidence=forecast.get("confidence", 0.90),
            metrics=metrics,
        )

sales_agent = SalesAgent()