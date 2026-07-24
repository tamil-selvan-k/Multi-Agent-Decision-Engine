
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import numpy as np

def fetch_budget():
    """
    Fetch department budgets and current spending.
    Initializes FinancialHistory and BudgetData if empty.
    """

    db = SessionLocal()

    try:
        # ------------------------------------------------------------------
        # STEP 1: Populate FinancialHistory (only once)
        # ------------------------------------------------------------------
        history = db.query(models.FinancialHistory).all()

        if not history:

            sample_data = [
                ("Jan", "sales", 500000, 420000, 650000, 180000, 240000),
                ("Feb", "sales", 500000, 435000, 670000, 185000, 250000),
                ("Mar", "sales", 500000, 450000, 690000, 190000, 260000),

                ("Jan", "inventory", 300000, 250000, 380000, 120000, 110000),
                ("Feb", "inventory", 300000, 265000, 390000, 125000, 115000),
                ("Mar", "inventory", 300000, 280000, 410000, 130000, 120000),

                ("Jan", "finance", 200000, 160000, 270000, 80000, 60000),
                ("Feb", "finance", 200000, 170000, 280000, 85000, 65000),
                ("Mar", "finance", 200000, 180000, 290000, 90000, 70000),

                ("Jan", "logistics", 250000, 200000, 330000, 100000, 85000),
                ("Feb", "logistics", 250000, 210000, 340000, 105000, 90000),
                ("Mar", "logistics", 250000, 220000, 350000, 110000, 95000),
            ]

            for row in sample_data:
                db.add(
                    models.FinancialHistory(
                        month=row[0],
                        department=row[1],
                        budget=row[2],
                        spending=row[3],
                        revenue=row[4],
                        operational_cost=row[5],
                        procurement_cost=row[6],
                    )
                )

            db.commit()

        # ------------------------------------------------------------------
        # STEP 2: Populate BudgetData using latest month
        # ------------------------------------------------------------------
        if db.query(models.BudgetData).count() == 0:

            latest = (
                db.query(models.FinancialHistory)
                .filter(models.FinancialHistory.month == "Mar")
                .all()
            )

            for item in latest:
                db.add(
                    models.BudgetData(
                        department=item.department,
                        budget=item.budget,
                        spending=item.spending,
                    )
                )

            db.commit()

        # ------------------------------------------------------------------
        # STEP 3: Return existing interface
        # ------------------------------------------------------------------
        budget_entries = db.query(models.BudgetData).all()

        department_budgets = {}
        current_spending = {}

        for entry in budget_entries:
            department_budgets[entry.department] = entry.budget
            current_spending[entry.department] = entry.spending

        return {
            "department_budgets": department_budgets,
            "current_spending": current_spending,
        }

    finally:
        db.close()

def anomaly_detection():
    """
    Detect anomalous spending using Isolation Forest.
    """

    db = SessionLocal()

    try:
        history = db.query(models.FinancialHistory).all()

        df = pd.DataFrame([
        {
        "budget": row.budget,
        "spending": row.spending,
        "revenue": row.revenue,
        "operational_cost": row.operational_cost,
        "procurement_cost": row.procurement_cost,
        }
        for row in history
])

        model = IsolationForest(
            contamination=0.1,
            random_state=42
        )

        features = df[
    [
        "budget",
        "spending",
        "revenue",
        "operational_cost",
        "procurement_cost",
    ]
]

        predictions = model.fit_predict(features)
        scores = model.decision_function(features)

        anomaly_exists = (-1 in predictions)
        anomaly_score = float(scores.min())

        record = db.query(models.AnomalyData).first()

        if record:
            record.anomaly = anomaly_exists
            record.score = anomaly_score
        else:
            record = models.AnomalyData(
                anomaly=anomaly_exists,
                score=anomaly_score
            )
            db.add(record)

        db.commit()

        return {
            "anomaly": anomaly_exists,
            "score": anomaly_score
        }

    finally:
        db.close()

def cost_estimator():
    """
    Predict next month's operational cost using Linear Regression.
    """

    db = SessionLocal()

    try:
        history = (
            db.query(models.FinancialHistory)
            .order_by(models.FinancialHistory.id)
            .all()
        )

        if len(history) < 2:
            return {"extra_cost": 0}

        # -----------------------------
        # Prepare training data
        # -----------------------------
        X = np.array([
            [
                row.budget,
                row.spending,
                row.revenue,
                row.procurement_cost,
            ]
            for row in history
        ])

        y = np.array([
            row.operational_cost
            for row in history
        ])

        # -----------------------------
        # Train Linear Regression model
        # -----------------------------
        model = LinearRegression()
        model.fit(X, y)

        # -----------------------------
        # Predict next month's cost
        # -----------------------------
        last = history[-1]

        next_input = np.array([[
            last.budget,
            last.spending,
            last.revenue,
            last.procurement_cost,
        ]])

        predicted_cost = int(model.predict(next_input)[0])

        # -----------------------------
        # Save prediction
        # -----------------------------
        record = db.query(models.CostEstimate).first()

        if record:
            record.extra_cost = predicted_cost
        else:
            record = models.CostEstimate(
                extra_cost=predicted_cost
            )
            db.add(record)

        db.commit()

        return {
            "extra_cost": predicted_cost
        }

    finally:
        db.close()

def budget_impact():
    """
    Calculate the impact of the predicted operational cost on the enterprise budget.
    """

    db = SessionLocal()

    try:
        # Get latest budgets
        budget_entries = db.query(models.BudgetData).all()

        total_budget = sum(entry.budget for entry in budget_entries)
        total_spending = sum(entry.spending for entry in budget_entries)

        # Get predicted cost from Linear Regression
        cost_record = db.query(models.CostEstimate).first()

        if cost_record:
            predicted_cost = cost_record.extra_cost
        else:
            predicted_cost = 0

        # Financial calculations
        projected_spending = total_spending + predicted_cost

        budget_exceeded = projected_spending > total_budget

        remaining_budget = total_budget - projected_spending

        cashflow = "Positive" if remaining_budget >= 0 else "Negative"

        # Save / Update database
        impact = db.query(models.BudgetImpact).first()

        if impact:
            impact.budget_exceeded = budget_exceeded
            impact.remaining_budget = remaining_budget
            impact.cashflow = cashflow
        else:
            impact = models.BudgetImpact(
                budget_exceeded=budget_exceeded,
                remaining_budget=remaining_budget,
                cashflow=cashflow,
            )
            db.add(impact)

        db.commit()

        return {
            "budget_exceeded": budget_exceeded,
            "remaining_budget": remaining_budget,
            "cashflow": cashflow,
        }

    finally:
        db.close()

def calculate_roi():
    """
    Calculate Return on Investment (ROI).
    """

    db = SessionLocal()

    try:
        history = db.query(models.FinancialHistory).all()

        total_revenue = sum(row.revenue for row in history)

        cost_record = db.query(models.CostEstimate).first()

        predicted_cost = cost_record.extra_cost if cost_record else 0

        if predicted_cost == 0:
            roi = 0
        else:
            roi = ((total_revenue - predicted_cost) / predicted_cost) * 100

        expected_return = total_revenue - predicted_cost

        profitable = roi > 0

        record = db.query(models.FinancialROI).first()

        if record:
            record.roi = roi
            record.profitable = profitable
            record.expected_return = expected_return
        else:
            record = models.FinancialROI(
                roi=roi,
                profitable=profitable,
                expected_return=expected_return,
            )
            db.add(record)

        db.commit()

        return {
            "roi": round(roi, 2),
            "profitable": profitable,
            "expected_return": expected_return,
        }

    finally:
        db.close()

def financial_risk_score():
    """
    Calculate an overall financial risk score using
    anomaly detection, budget impact, and ROI.
    """

    db = SessionLocal()

    try:
        anomaly = db.query(models.AnomalyData).first()
        impact = db.query(models.BudgetImpact).first()
        roi = db.query(models.FinancialROI).first()

        score = 0

        # -----------------------------
        # Anomaly contributes 40 points
        # -----------------------------
        if anomaly and anomaly.anomaly:
            score += 40

        # -----------------------------
        # Budget contributes 30 points
        # -----------------------------
        if impact and impact.budget_exceeded:
            score += 30

        # -----------------------------
        # ROI contributes 30 points
        # -----------------------------
        if roi:
            if roi.roi < 10:
                score += 30
            elif roi.roi < 30:
                score += 20
            elif roi.roi < 50:
                score += 10

        # -----------------------------
        # Determine risk level
        # -----------------------------
        if score >= 60:
            risk_level = "High"
        elif score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        record = db.query(models.FinancialRisk).first()

        if record:
            record.risk_score = score
            record.risk_level = risk_level
        else:
            record = models.FinancialRisk(
                risk_score=score,
                risk_level=risk_level,
            )
            db.add(record)

        db.commit()

        return {
            "risk_score": score,
            "risk_level": risk_level,
        }

    finally:
        db.close()