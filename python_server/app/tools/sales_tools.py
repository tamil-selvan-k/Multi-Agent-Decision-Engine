def fetch_sales_data():
    """Fetch sales data from PostgreSQL/ERP.

    Returns:
        list: List of dicts with date and sales.
    """
    # Mock data as per spec
    return [
        {
            "date": "2025-01",
            "sales": 2200
        },
        {
            "date": "2025-02",
            "sales": 2350
        },
        {
            "date": "2025-03",
            "sales": 2400
        }
    ]


def forecast_demand():
    """Use Prophet to forecast demand.

    Returns:
        dict: forecast and confidence.
    """
    return {
        "forecast": 2650,
        "confidence": 0.93
    }


def calculate_growth():
    """Simple analytics to calculate growth.

    Returns:
        dict: growth percentage.
    """
    return {
        "growth": 18.2
    }


def recommend_production():
    """Business logic to recommend production change.

    Returns:
        str: recommendation like \"Increase production by 12%\".
    """
    # In a real scenario, this would use forecast, inventory, etc.
    return "Increase production by 12%"