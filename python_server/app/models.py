from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from core.database import Base, engine

class SalesData(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)  # storing as string for simplicity, e.g., "2025-01"
    sales = Column(Integer)

class ForecastData(Base):
    __tablename__ = "forecast_data"

    id = Column(Integer, primary_key=True, index=True)
    forecast = Column(Integer)
    confidence = Column(Float)

class GrowthData(Base):
    __tablename__ = "growth_data"

    id = Column(Integer, primary_key=True, index=True)
    growth = Column(Float)

class ProductionRecommendation(Base):
    __tablename__ = "production_recommendation"

    id = Column(Integer, primary_key=True, index=True)
    recommendation = Column(String)

class InventoryData(Base):
    __tablename__ = "inventory_data"

    id = Column(Integer, primary_key=True, index=True)
    current_stock = Column(Integer)
    warehouse_capacity = Column(Integer)
    safety_stock = Column(Integer)

class OptimizationData(Base):
    __tablename__ = "optimization_data"

    id = Column(Integer, primary_key=True, index=True)
    recommended_stock = Column(Integer)

class WarehouseCapacity(Base):
    __tablename__ = "warehouse_capacity"

    id = Column(Integer, primary_key=True, index=True)
    utilization = Column(Integer)

class ReorderRecommendation(Base):
    __tablename__ = "reorder_recommendation"

    id = Column(Integer, primary_key=True, index=True)
    recommendation = Column(String)

class BudgetData(Base):
    __tablename__ = "budget_data"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)
    budget = Column(Integer)
    spending = Column(Integer)

class AnomalyData(Base):
    __tablename__ = "anomaly_data"

    id = Column(Integer, primary_key=True, index=True)
    anomaly = Column(Boolean)
    score = Column(Float)

class CostEstimate(Base):
    __tablename__ = "cost_estimate"

    id = Column(Integer, primary_key=True, index=True)
    extra_cost = Column(Integer)

class BudgetImpact(Base):
    __tablename__ = "budget_impact"

    id = Column(Integer, primary_key=True, index=True)
    budget_exceeded = Column(Boolean)
    remaining_budget = Column(Integer)
    cashflow = Column(String)

class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(String, index=True)
    origin = Column(String)
    destination = Column(String)
    status = Column(String)

class RouteOptimization(Base):
    __tablename__ = "route_optimization"

    id = Column(Integer, primary_key=True, index=True)
    best_route = Column(String)  # storing as JSON string or comma-separated
    total_distance_km = Column(Integer)

class DeliveryETA(Base):
    __tablename__ = "delivery_eta"

    id = Column(Integer, primary_key=True, index=True)
    estimated_delivery_hours = Column(Integer)
    delay_probability = Column(Float)

class WarehouseAssignment(Base):
    __tablename__ = "warehouse_assignment"

    id = Column(Integer, primary_key=True, index=True)
    recommended_warehouse = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)