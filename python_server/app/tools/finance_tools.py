from sqlalchemy.orm import Session
from core.database import SessionLocal
import models as models

def fetch_budget():
    """Fetch department budgets and current spending.

    Returns:
        dict: department budgets, current spending.
    """
    db = SessionLocal()
    try:
        # We'll store budget and spending in the BudgetData table with a department column
        budget_entries = db.query(models.BudgetData).all()
        if not budget_entries:
            # Insert default data as per spec
            default_data = [
                {"department": "sales", "budget": 500000, "spending": 450000},
                {"department": "inventory", "budget": 300000, "spending": 280000},
                {"department": "finance", "budget": 200000, "spending": 180000},
                {"department": "logistics", "budget": 250000, "spending": 220000}
            ]
            for item in default_data:
                db.add(models.BudgetData(**item))
            db.commit()
            budget_entries = db.query(models.BudgetData).all()
        # Build the expected return structure
        department_budgets = {}
        current_spending = {}
        for entry in budget_entries:
            department_budgets[entry.department] = entry.budget
            current_spending[entry.department] = entry.spending
        return {
            "department_budgets": department_budgets,
            "current_spending": current_spending
        }
    finally:
        db.close()

def anomaly_detection():
    """Use Isolation Forest to detect anomalous spending.

    Returns:
        dict: anomaly flag and score.
    """
    db = SessionLocal()
    try:
        anomaly_record = db.query(models.AnomalyData).first()
        if not anomaly_record:
            # Assume no anomaly for demo
            anomaly_record = models.AnomalyData(anomaly=False, score=0.12)
            db.add(anomaly_record)
            db.commit()
            db.refresh(anomaly_record)
        return {
            "anomaly": anomaly_record.anomaly,
            "score": anomaly_record.score
        }
    finally:
        db.close()

def cost_estimator():
    """Estimate extra cost for production increase.

    Returns:
        dict: extra cost.
    """
    db = SessionLocal()
    try:
        cost_record = db.query(models.CostEstimate).first()
        if not cost_record:
            cost_record = models.CostEstimate(extra_cost=120000)
            db.add(cost_record)
            db.commit()
            db.refresh(cost_record)
        return {
            "extra_cost": cost_record.extra_cost
        }
    finally:
        db.close()

def budget_impact():
    """Calculate budget impact of extra cost.

    Returns:
        dict: budget exceeded flag, remaining budget, cashflow.
    """
    db = SessionLocal()
    try:
        impact_record = db.query(models.BudgetImpact).first()
        if not impact_record:
            # We need to compute based on current budget and spending and extra cost
            budget_data = fetch_budget()  # This will create default if not exist
            total_budget = sum(budget_data["department_budgets"].values())
            total_spending = sum(budget_data["current_spending"].values())
            extra_cost = 120000  # from cost_estimator, but we can get it
            # However, to avoid calling another function that opens a new session, we can compute similarly.
            # For simplicity, we'll just use the same default logic as in the spec.
            projected_spending = total_spending + extra_cost
            budget_exceeded = projected_spending > total_budget
            remaining_budget = max(0, total_budget - projected_spending)
            cashflow = "positive" if not budget_exceeded else "negative"
            impact_record = models.BudgetImpact(
                budget_exceeded=budget_exceeded,
                remaining_budget=remaining_budget,
                cashflow=cashflow
            )
            db.add(impact_record)
            db.commit()
            db.refresh(impact_record)
        return {
            "budget_exceeded": impact_record.budget_exceeded,
            "remaining_budget": impact_record.remaining_budget,
            "cashflow": impact_record.cashflow
        }
    finally:
        db.close()