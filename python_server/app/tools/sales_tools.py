from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models
from app.core.database import SessionLocal
import app.models as models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_sales_data():
    """
    Fetch sales data. If the table is empty, populate it with sample records.

    Returns:
        list: List of sales records.
    """
    db = SessionLocal()

    try:
        existing = db.query(models.SalesData).all()

        if not existing:

            default_data = [
                {
                    "order_id": "ORD001",
                    "date": "2025-01",
                    "product_id": "P101",
                    "product_name": "Laptop",
                    "quantity": 15,
                    "selling_price": 55000,
                    "revenue": 825000,
                    "region": "North",
                    "sales": 825000,
                },
                {
                    "order_id": "ORD002",
                    "date": "2025-01",
                    "product_id": "P102",
                    "product_name": "Mouse",
                    "quantity": 120,
                    "selling_price": 800,
                    "revenue": 96000,
                    "region": "South",
                    "sales": 96000,
                },
                {
                    "order_id": "ORD003",
                    "date": "2025-02",
                    "product_id": "P103",
                    "product_name": "Keyboard",
                    "quantity": 80,
                    "selling_price": 1800,
                    "revenue": 144000,
                    "region": "East",
                    "sales": 144000,
                },
                {
                    "order_id": "ORD004",
                    "date": "2025-02",
                    "product_id": "P101",
                    "product_name": "Laptop",
                    "quantity": 18,
                    "selling_price": 55000,
                    "revenue": 990000,
                    "region": "West",
                    "sales": 990000,
                },
                {
                    "order_id": "ORD005",
                    "date": "2025-03",
                    "product_id": "P104",
                    "product_name": "Monitor",
                    "quantity": 30,
                    "selling_price": 12000,
                    "revenue": 360000,
                    "region": "North",
                    "sales": 360000,
                },
                {
                    "order_id": "ORD006",
                    "date": "2025-03",
                    "product_id": "P102",
                    "product_name": "Mouse",
                    "quantity": 150,
                    "selling_price": 800,
                    "revenue": 120000,
                    "region": "South",
                    "sales": 120000,
                },
                {
                    "order_id": "ORD007",
                    "date": "2025-04",
                    "product_id": "P101",
                    "product_name": "Laptop",
                    "quantity": 20,
                    "selling_price": 56000,
                    "revenue": 1120000,
                    "region": "East",
                    "sales": 1120000,
                },
                {
                    "order_id": "ORD008",
                    "date": "2025-04",
                    "product_id": "P105",
                    "product_name": "Printer",
                    "quantity": 25,
                    "selling_price": 9000,
                    "revenue": 225000,
                    "region": "West",
                    "sales": 225000,
                },
            ]

            for item in default_data:
                db.add(models.SalesData(**item))

            db.commit()

        sales_records = db.query(models.SalesData).all()

        return [
            {
                "order_id": row.order_id,
                "date": row.date,
                "product_id": row.product_id,
                "product_name": row.product_name,
                "quantity": row.quantity,
                "selling_price": row.selling_price,
                "revenue": row.revenue,
                "region": row.region,
                "sales": row.sales,
            }
            for row in sales_records
        ]

    finally:
        db.close()

def forecast_demand():
    db = SessionLocal()

    try:
        sales_records = (
            db.query(models.SalesData)
            .order_by(models.SalesData.date)
            .all()
        )

        if not sales_records:
            return {"forecast": 0, "confidence": 0}

        # Monthly sales aggregation
        monthly_sales = {}

        for record in sales_records:
            monthly_sales.setdefault(record.date, 0)
            monthly_sales[record.date] += record.sales

        months = sorted(monthly_sales.keys())
        monthly_values = [monthly_sales[m] for m in months]

        average_monthly_sales = sum(monthly_values) / len(monthly_values)

        if len(monthly_values) > 1:
            trend = monthly_values[-1] - monthly_values[-2]
        else:
            trend = 0

        forecast = round(
            average_monthly_sales + (0.5 * trend),
            2
        )

        confidence = round(
            min(0.75 + (len(monthly_values) * 0.05), 0.98),
            2
        )

        existing = db.query(models.ForecastData).first()

        if existing:
            existing.forecast = forecast
            existing.confidence = confidence
        else:
            db.add(
                models.ForecastData(
                    forecast=forecast,
                    confidence=confidence,
                )
            )

        db.commit()

        return {
            "forecast": forecast,
            "confidence": confidence,
        }

    finally:
        db.close()

def calculate_growth():
    db = SessionLocal()

    try:
        sales_records = (
            db.query(models.SalesData)
            .order_by(models.SalesData.date)
            .all()
        )

        if not sales_records:
            return {"growth": 0}

        # Monthly total sales
        monthly_sales = {}

        for record in sales_records:
            monthly_sales.setdefault(record.date, 0)
            monthly_sales[record.date] += record.sales

        months = sorted(monthly_sales.keys())

        first_month_sales = monthly_sales[months[0]]
        last_month_sales = monthly_sales[months[-1]]

        if first_month_sales == 0:
            growth = 0
        else:
            growth = round(
                ((last_month_sales - first_month_sales) / first_month_sales) * 100,
                2
            )

        existing = db.query(models.GrowthData).first()

        if existing:
            existing.growth = growth
        else:
            db.add(models.GrowthData(growth=growth))

        db.commit()

        return {
            "growth": growth
        }

    finally:
        db.close()

def recommend_production():
    db = SessionLocal()

    try:
        forecast_data = db.query(models.ForecastData).first()
        growth_data = db.query(models.GrowthData).first()
        sales_records = db.query(models.SalesData).all()

        if not forecast_data or not growth_data or not sales_records:
            return {"recommendation": "Insufficient data"}

        # Monthly sales aggregation
        monthly_sales = {}

        for record in sales_records:
            monthly_sales.setdefault(record.date, 0)
            monthly_sales[record.date] += record.sales

        average_monthly_sales = (
            sum(monthly_sales.values()) / len(monthly_sales)
            if monthly_sales
            else 0
        )

        forecast = forecast_data.forecast
        growth = growth_data.growth

        if (
            forecast > average_monthly_sales * 1.10
            and growth > 10
        ):
            recommendation = "Increase production by 15%"

        elif (
            forecast < average_monthly_sales * 0.90
            and growth < 0
        ):
            recommendation = "Reduce production by 10%"

        else:
            recommendation = "Maintain current production"

        existing = db.query(models.ProductionRecommendation).first()

        if existing:
            existing.recommendation = recommendation
        else:
            db.add(
                models.ProductionRecommendation(
                    recommendation=recommendation
                )
            )

        db.commit()

        return {
            "recommendation": recommendation,
            "average_monthly_sales": round(average_monthly_sales, 2),
            "forecast": forecast,
            "growth": growth,
        }

    finally:
        db.close()

def revenue_analysis():
    """
    Analyze revenue metrics from sales data.

    Returns:
        dict: Revenue statistics.
    """
    db = SessionLocal()

    try:
        sales = db.query(models.SalesData).all()

        if not sales:
            total_revenue = 0
            average_order_value = 0
            highest_sale = 0
        else:
            total_revenue = sum(record.revenue for record in sales)
            average_order_value = round(
                total_revenue / len(sales),
                2
            )
            highest_sale = max(record.revenue for record in sales)

        existing = db.query(models.RevenueAnalysis).first()

        if existing:
            existing.total_revenue = total_revenue
            existing.average_order_value = average_order_value
            existing.highest_sale = highest_sale
        else:
            existing = models.RevenueAnalysis(
                total_revenue=total_revenue,
                average_order_value=average_order_value,
                highest_sale=highest_sale,
            )
            db.add(existing)

        db.commit()
        db.refresh(existing)

        return {
            "total_revenue": existing.total_revenue,
            "average_order_value": existing.average_order_value,
            "highest_sale": existing.highest_sale,
        }

    finally:
        db.close()

def top_selling_products():
    """
    Identify the top-selling product.

    Returns:
        dict: Product with the highest units sold.
    """
    db = SessionLocal()

    try:
        sales = db.query(models.SalesData).all()

        if not sales:
            product_id = "N/A"
            product_name = "No Data"
            units_sold = 0

        else:
            product_summary = {}

            for record in sales:

                if record.product_id not in product_summary:
                    product_summary[record.product_id] = {
                        "product_name": record.product_name,
                        "units_sold": 0,
                    }

                product_summary[record.product_id]["units_sold"] += record.quantity

            best_product = max(
                product_summary.items(),
                key=lambda item: item[1]["units_sold"]
            )

            product_id = best_product[0]
            product_name = best_product[1]["product_name"]
            units_sold = best_product[1]["units_sold"]

        existing = db.query(models.TopSellingProduct).first()

        if existing:
            existing.product_id = product_id
            existing.product_name = product_name
            existing.units_sold = units_sold

        else:
            existing = models.TopSellingProduct(
                product_id=product_id,
                product_name=product_name,
                units_sold=units_sold,
            )
            db.add(existing)

        db.commit()
        db.refresh(existing)

        return {
            "product_id": existing.product_id,
            "product_name": existing.product_name,
            "units_sold": existing.units_sold,
        }

    finally:
        db.close()