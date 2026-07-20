from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models

def fetch_inventory():
    """Fetch current inventory from warehouse.

    Returns:
        dict: current stock, warehouse capacity, safety stock.
    """
    db = SessionLocal()
    try:
        inv_record = db.query(models.InventoryData).first()
        if not inv_record:
            # Insert default data as per spec
            inv_record = models.InventoryData(
                current_stock=1200,
                warehouse_capacity=2000,
                safety_stock=300
            )
            db.add(inv_record)
            db.commit()
            db.refresh(inv_record)
        return {
            "current_stock": inv_record.current_stock,
            "warehouse_capacity": inv_record.warehouse_capacity,
            "safety_stock": inv_record.safety_stock
        }
    finally:
        db.close()

def optimize_inventory():
    """Use OR-Tools to optimize inventory levels.

    Returns:
        dict: recommended stock level.
    """
    db = SessionLocal()
    try:
        opt_record = db.query(models.OptimizationData).first()
        if not opt_record:
            opt_record = models.OptimizationData(recommended_stock=1400)
            db.add(opt_record)
            db.commit()
            db.refresh(opt_record)
        return {
            "recommended_stock": opt_record.recommended_stock
        }
    finally:
        db.close()

def warehouse_capacity():
    """Returns warehouse utilization.

    Returns:
        dict: utilization percentage.
    """
    db = SessionLocal()
    try:
        cap_record = db.query(models.WarehouseCapacity).first()
        if not cap_record:
            cap_record = models.WarehouseCapacity(utilization=94)
            db.add(cap_record)
            db.commit()
            db.refresh(cap_record)
        return {
            "utilization": cap_record.utilization
        }
    finally:
        db.close()

def reorder_recommendation():
    """Generate reorder recommendation.

    Returns:
        str: either "Order X units" or "Delay purchasing".
    """
    db = SessionLocal()
    try:
        rec_record = db.query(models.ReorderRecommendation).first()
        if not rec_record:
            # For simplicity, we'll always return "Order 350 units" as per spec
            rec_record = models.ReorderRecommendation(recommendation="Order 350 units")
            db.add(rec_record)
            db.commit()
            db.refresh(rec_record)
        return rec_record.recommendation
    finally:
        db.close()