def fetch_budget():
    """Fetch department budgets and current spending.

    Returns:
        dict: department budgets, current spending.
    """
    return {
        "department_budgets": {
            "sales": 500000,
            "inventory": 300000,
            "finance": 200000,
            "logistics": 250000
        },
        "current_spending": {
            "sales": 450000,
            "inventory": 280000,
            "finance": 180000,
            "logistics": 220000
        }
    }


def anomaly_detection():
    """Use Isolation Forest to detect anomalous spending.

    Returns:
        dict: anomaly flag and score.
    """
    # Mock detection: assume no anomaly for demo
    return {
        "anomaly": False,
        "score": 0.12
    }


def cost_estimator():
    """Estimate extra cost for production increase.

    Returns:
        dict: extra cost.
    """
    return {
        "extra_cost": 120000
    }


def budget_impact():
    """Calculate budget impact of extra cost.

    Returns:
        dict: budget exceeded flag, remaining budget, cashflow.
    """
    # Simple calculation: assume total budget is sum of department budgets
    budget_data = fetch_budget()
    total_budget = sum(budget_data["department_budgets"].values())
    total_spending = sum(budget_data["current_spending"].values())
    extra_cost = 120000  # from cost_estimator, but we could call it; for simplicity use fixed
    projected_spending = total_spending + extra_cost
    budget_exceeded = projected_spending > total_budget
    remaining_budget = max(0, total_budget - projected_spending)

    return {
        "budget_exceeded": budget_exceeded,
        "remaining_budget": remaining_budget,
        "cashflow": "positive" if not budget_exceeded else "negative"
    }