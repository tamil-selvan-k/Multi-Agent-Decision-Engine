from app.tools.sales_tools import (
    fetch_sales_data,
    forecast_demand,
    calculate_growth,
    revenue_analysis,
    top_selling_products,
    recommend_production,
)

from app.schemas.recommendation import AgentRecommendation


class SalesAgent:
    def __init__(self, name: str = "SalesAgent"):
        self.name = name

    def run(self) -> AgentRecommendation:
        """
        Run the Sales Agent.

        Returns:
            AgentRecommendation: Sales analysis and recommendation details.
        """

        sales_data = fetch_sales_data()

        forecast = forecast_demand()

        growth = calculate_growth()

        revenue = revenue_analysis()

        top_product = top_selling_products()

        production = recommend_production()

        recommendation = (
            f"Processed {len(sales_data)} sales records. "
            f"Forecasted sales: ₹{forecast['forecast']:.2f}. "
            f"Growth: {growth['growth']:.2f}%. "
            f"Total Revenue: ₹{revenue['total_revenue']:.2f}. "
            f"Average Order Value: ₹{revenue['average_order_value']:.2f}. "
            f"Highest Sale: ₹{revenue['highest_sale']:.2f}. "
            f"Top Selling Product: {top_product['product_name']} "
            f"({top_product['units_sold']} units). "
            f"Recommendation: {production['recommendation']}."
        )

        metrics = {
            "sales_records": len(sales_data),
            "forecast": forecast,
            "growth": growth,
            "revenue": revenue,
            "top_selling_product": top_product,
            "production_recommendation": production,
        }

        # Retrieve confidence score from the forecast model
        confidence = float(forecast.get("confidence", 0.90))

        return AgentRecommendation(
            agent_name=self.name,
            recommendation=recommendation,
            confidence=confidence,
            metrics=metrics,
        )


sales_agent = SalesAgent()