from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models
from sklearn.linear_model import LinearRegression
import numpy as np

def fetch_inventory():
    """
    Fetch inventory data from database.
    Seeds InventoryHistory if empty and updates InventoryData.
    """

    db = SessionLocal()

    try:
        # Seed historical inventory if empty
        if db.query(models.InventoryHistory).count() == 0:

            sample_data = [
                ("Jan", 1500, 420, 300, 2000, 300),
                ("Feb", 1450, 470, 350, 2000, 300),
                ("Mar", 1380, 520, 450, 2000, 300),
                ("Apr", 1320, 510, 400, 2000, 300),
                ("May", 1280, 540, 450, 2000, 300),
                ("Jun", 1210, 560, 500, 2000, 300),
                ("Jul", 1180, 590, 550, 2000, 300),
                ("Aug", 1150, 610, 500, 2000, 300),
                ("Sep", 1100, 630, 550, 2000, 300),
                ("Oct", 1070, 650, 600, 2000, 300),
                ("Nov", 1020, 690, 650, 2000, 300),
                ("Dec", 980, 720, 700, 2000, 300),
            ]

            for month, stock, sold, incoming, capacity, safety in sample_data:
                db.add(
                    models.InventoryHistory(
                        month=month,
                        current_stock=stock,
                        sold=sold,
                        incoming_stock=incoming,
                        warehouse_capacity=capacity,
                        safety_stock=safety,
                    )
                )

            db.commit()

        # Latest inventory record
        latest = (
            db.query(models.InventoryHistory)
            .order_by(models.InventoryHistory.id.desc())
            .first()
        )

        inventory = db.query(models.InventoryData).first()

        if inventory is None:
            inventory = models.InventoryData(
                current_stock=latest.current_stock,
                warehouse_capacity=latest.warehouse_capacity,
                safety_stock=latest.safety_stock,
            )
            db.add(inventory)
        else:
            inventory.current_stock = latest.current_stock
            inventory.warehouse_capacity = latest.warehouse_capacity
            inventory.safety_stock = latest.safety_stock

        db.commit()
        db.refresh(inventory)

        return {
            "current_stock": inventory.current_stock,
            "warehouse_capacity": inventory.warehouse_capacity,
            "safety_stock": inventory.safety_stock,
        }

    finally:
        db.close()

def demand_forecast():
    """
    Predict next month's inventory demand using Linear Regression.
    """

    db = SessionLocal()

    try:
        history = db.query(models.InventoryHistory).order_by(models.InventoryHistory.id).all()

        months = np.arange(len(history)).reshape(-1, 1)
        demand = np.array([record.sold for record in history])

        model = LinearRegression()
        model.fit(months, demand)

        next_month = np.array([[len(history)]])
        predicted_demand = int(model.predict(next_month)[0])

        forecast = db.query(models.DemandForecast).first()

        if forecast is None:
            forecast = models.DemandForecast(
                predicted_demand=predicted_demand
            )
            db.add(forecast)
        else:
            forecast.predicted_demand = predicted_demand

        db.commit()
        db.refresh(forecast)

        return {
            "predicted_demand": forecast.predicted_demand
        }

    finally:
        db.close()

def warehouse_capacity():
    """
    Calculate warehouse utilization.
    """

    db = SessionLocal()

    try:
        inventory = db.query(models.InventoryData).first()

        utilization = (
            inventory.current_stock / inventory.warehouse_capacity
        ) * 100

        status = (
            "High"
            if utilization >= 90
            else "Medium"
            if utilization >= 70
            else "Low"
        )

        warehouse = db.query(models.WarehouseCapacity).first()

        if warehouse is None:
            warehouse = models.WarehouseCapacity(
                utilization=utilization,
                status=status,
            )
            db.add(warehouse)
        else:
            warehouse.utilization = utilization
            warehouse.status = status

        db.commit()
        db.refresh(warehouse)

        return {
            "utilization": round(warehouse.utilization, 2),
            "status": warehouse.status,
        }

    finally:
        db.close()

def reorder_recommendation():
    """
    Generate reorder recommendation based on inventory and predicted demand.
    """

    db = SessionLocal()

    try:
        inventory = db.query(models.InventoryData).first()
        forecast = db.query(models.DemandForecast).first()

        available_stock = inventory.current_stock
        safety_stock = inventory.safety_stock
        predicted_demand = forecast.predicted_demand

        reorder = predicted_demand > (available_stock - safety_stock)

        if reorder:
            quantity = predicted_demand + safety_stock - available_stock

            if quantity >= 300:
                priority = "High"
            elif quantity >= 150:
                priority = "Medium"
            else:
                priority = "Low"
        else:
            quantity = 0
            priority = "None"

        recommendation = db.query(models.ReorderRecommendation).first()

        if recommendation is None:
            recommendation = models.ReorderRecommendation(
                reorder=reorder,
                quantity=quantity,
                priority=priority
            )
            db.add(recommendation)
        else:
            recommendation.reorder = reorder
            recommendation.quantity = quantity
            recommendation.priority = priority

        db.commit()
        db.refresh(recommendation)

        return {
            "reorder": recommendation.reorder,
            "quantity": recommendation.quantity,
            "priority": recommendation.priority
        }

    finally:
        db.close()

def supplier_recommendation():

    db = SessionLocal()

    try:

        if db.query(models.Supplier).count() == 0:

            suppliers = [

                models.Supplier(
                    name="Supplier A",
                    lead_time=5,
                    cost_per_unit=120,
                    reliability=0.97,
                    rating=4.8,
                    quality_score=95,
                    on_time_delivery=98,
                    available_stock=1200
                ),

                models.Supplier(
                    name="Supplier B",
                    lead_time=3,
                    cost_per_unit=135,
                    reliability=0.92,
                    rating=4.6,
                    quality_score=91,
                    on_time_delivery=94,
                    available_stock=700
                ),

                models.Supplier(
                    name="Supplier C",
                    lead_time=7,
                    cost_per_unit=105,
                    reliability=0.88,
                    rating=4.3,
                    quality_score=89,
                    on_time_delivery=90,
                    available_stock=2500
                )
            ]

            db.add_all(suppliers)
            db.commit()

        reorder = db.query(models.ReorderRecommendation).first()

        suppliers = db.query(models.Supplier).all()

        candidates = []

        for supplier in suppliers:

            if supplier.available_stock < reorder.quantity:
                continue

            score = (
                supplier.reliability * 35 +
                supplier.quality_score * 0.20 +
                supplier.on_time_delivery * 0.15 +
                supplier.rating * 5 -
                supplier.cost_per_unit * 0.05 -
                supplier.lead_time
            )

            candidates.append((score, supplier))

        score, best = max(candidates, key=lambda x: x[0])

        estimated_cost = reorder.quantity * best.cost_per_unit

        recommendation = db.query(models.SupplierRecommendation).first()

        reason = (
            "Best balance of reliability, quality, delivery performance, lead time and procurement cost."
        )

        if recommendation is None:

            recommendation = models.SupplierRecommendation(
                supplier=best.name,
                quantity=reorder.quantity,
                estimated_cost=estimated_cost,
                lead_time=best.lead_time,
                score=round(score,2),
                reason=reason
            )

            db.add(recommendation)

        else:

            recommendation.supplier = best.name
            recommendation.quantity = reorder.quantity
            recommendation.estimated_cost = estimated_cost
            recommendation.lead_time = best.lead_time
            recommendation.score = round(score,2)
            recommendation.reason = reason

        db.commit()
        db.refresh(recommendation)

        return {

            "supplier": recommendation.supplier,

            "quantity": recommendation.quantity,

            "estimated_cost": recommendation.estimated_cost,

            "lead_time": recommendation.lead_time,

            "score": recommendation.score,

            "reason": recommendation.reason

        }

    finally:

        db.close()

def inventory_risk_score():
    """
    Calculate inventory risk based on inventory, warehouse,
    reorder requirement and supplier performance.
    """

    db = SessionLocal()

    try:

        inventory = db.query(models.InventoryData).first()
        warehouse = db.query(models.WarehouseCapacity).first()
        reorder = db.query(models.ReorderRecommendation).first()
        supplier = db.query(models.SupplierRecommendation).first()

        supplier_info = (
            db.query(models.Supplier)
            .filter(models.Supplier.name == supplier.supplier)
            .first()
        )

        risk = 0

        # Low stock
        if inventory.current_stock <= inventory.safety_stock:
            risk += 40

        # Warehouse nearly full
        if warehouse.utilization >= 90:
            risk += 20

        # Reorder required
        if reorder.reorder:
            risk += 20

        # Supplier reliability
        if supplier_info.reliability < 0.90:
            risk += 20

        # Long lead time
        if supplier_info.lead_time > 7:
            risk += 10

        if risk >= 60:
            level = "High"
        elif risk >= 30:
            level = "Medium"
        else:
            level = "Low"

        risk_record = db.query(models.InventoryRisk).first()

        if risk_record is None:
            risk_record = models.InventoryRisk(
                risk_score=risk,
                risk_level=level
            )
            db.add(risk_record)
        else:
            risk_record.risk_score = risk
            risk_record.risk_level = level

        db.commit()
        db.refresh(risk_record)

        return {
            "risk_score": risk_record.risk_score,
            "risk_level": risk_record.risk_level
        }

    finally:
        db.close()
        
def inventory_summary():
    """
    Generate an overall inventory summary.
    """

    db = SessionLocal()

    try:

        inventory = db.query(models.InventoryData).first()
        forecast = db.query(models.DemandForecast).first()
        warehouse = db.query(models.WarehouseCapacity).first()
        reorder = db.query(models.ReorderRecommendation).first()
        supplier = db.query(models.SupplierRecommendation).first()
        risk = db.query(models.InventoryRisk).first()

        # Inventory status
        if risk.risk_level == "High":
            status = "Critical"
        elif risk.risk_level == "Medium":
            status = "Warning"
        else:
            status = "Healthy"

        # Stockout prediction
        expected_stockout = (
            forecast.predicted_demand > inventory.current_stock
        )

        # Business recommendation
        if reorder.reorder:
            action = (
                f"Reorder {reorder.quantity} units from {supplier.supplier}. "
                f"Priority: {reorder.priority}. "
                f"Warehouse utilization is {warehouse.status}. "
                f"Inventory risk is {risk.risk_level}."
            )
        else:
            action = (
                f"No replenishment required. "
                f"Warehouse utilization is {warehouse.status}. "
                f"Inventory risk is {risk.risk_level}."
            )

        summary = db.query(models.InventorySummary).first()

        if summary is None:
            summary = models.InventorySummary(
                status=status,
                action=action,
                expected_stockout=expected_stockout
            )
            db.add(summary)
        else:
            summary.status = status
            summary.action = action
            summary.expected_stockout = expected_stockout

        db.commit()
        db.refresh(summary)

        return {
            "status": summary.status,
            "action": summary.action,
            "expected_stockout": summary.expected_stockout
        }

    finally:
        db.close()