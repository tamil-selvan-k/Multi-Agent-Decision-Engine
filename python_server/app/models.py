from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.core.database import Base, engine

class SalesData(Base):
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(String, nullable=False)

    date = Column(String, index=True, nullable=False)

    product_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    selling_price = Column(Float, nullable=False)

    revenue = Column(Float, nullable=False)

    region = Column(String, nullable=False)

    sales = Column(Float, nullable=False)

class ForecastData(Base):
    __tablename__ = "forecast_data"

    id = Column(Integer, primary_key=True, index=True)

    forecast = Column(Float)

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

class InventoryHistory(Base):
    __tablename__ = "inventory_history"

    id = Column(Integer, primary_key=True, index=True)

    month = Column(String)

    current_stock = Column(Integer)

    sold = Column(Integer)

    incoming_stock = Column(Integer)

    warehouse_capacity = Column(Integer)

    safety_stock = Column(Integer)

class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    lead_time = Column(Integer)          # days

    cost_per_unit = Column(Float)

    reliability = Column(Float)

    rating = Column(Float)

    quality_score = Column(Float)

    on_time_delivery = Column(Float)

    available_stock = Column(Integer)

class SupplierRecommendation(Base):
    __tablename__ = "supplier_recommendation"

    id = Column(Integer, primary_key=True, index=True)

    supplier = Column(String)

    quantity = Column(Integer)

    estimated_cost = Column(Float)

    lead_time = Column(Integer)

    score = Column(Float)

    reason = Column(String)

class DemandForecast(Base):
    __tablename__ = "demand_forecast"

    id = Column(Integer, primary_key=True, index=True)
    predicted_demand = Column(Integer)

class WarehouseCapacity(Base):
    __tablename__ = "warehouse_capacity"

    id = Column(Integer, primary_key=True, index=True)
    utilization = Column(Float)
    status = Column(String)

class ReorderRecommendation(Base):
    __tablename__ = "reorder_recommendation"

    id = Column(Integer, primary_key=True, index=True)
    reorder = Column(Boolean)
    quantity = Column(Integer)
    priority = Column(String)

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

class FinancialHistory(Base):
    __tablename__ = "financial_history"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, index=True)
    department = Column(String)
    budget = Column(Integer)
    spending = Column(Integer)
    revenue = Column(Integer)
    operational_cost = Column(Integer)
    procurement_cost = Column(Integer)

class FinancialRisk(Base):
    __tablename__ = "financial_risk"

    id = Column(Integer, primary_key=True, index=True)
    risk_score = Column(Float)
    risk_level = Column(String)

class FinancialROI(Base):
    __tablename__ = "financial_roi"

    id = Column(Integer, primary_key=True, index=True)
    roi = Column(Float)
    profitable = Column(Boolean)
    expected_return = Column(Integer)
    
class Shipment(Base):
    __tablename__ = "shipment"

    id = Column(Integer, primary_key=True, index=True)

    shipment_id = Column(String, unique=True, index=True)

    order_id = Column(String)

    supplier_id = Column(String)

    supplier_name = Column(String)

    warehouse_id = Column(String)

    origin = Column(String)

    destination = Column(String)

    vehicle_type = Column(String)

    distance_km = Column(Float)

    dispatch_date = Column(String)

    eta = Column(Float)

    actual_delivery_date = Column(String)

    transportation_cost = Column(Float)

    status = Column(String)

    delay_hours = Column(Float)

    lead_time = Column(Integer)

    supplier_reliability = Column(Float)

    quality_score = Column(Float)

    on_time_delivery = Column(Float)

    available_stock = Column(Integer)

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

class DeliveryRisk(Base):
    __tablename__ = "delivery_risk"

    id = Column(Integer, primary_key=True, index=True)

    risk_score = Column(Float)

    risk_level = Column(String)

    reason = Column(String)
class RevenueAnalysis(Base):
    __tablename__ = "revenue_analysis"

    id = Column(Integer, primary_key=True, index=True)
    total_revenue = Column(Float)
    average_order_value = Column(Float)
    highest_sale = Column(Float)

class TopSellingProduct(Base):
    __tablename__ = "top_selling_product"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String)
    product_name = Column(String)
    units_sold = Column(Integer)

# Create tables

Base.metadata.create_all(bind=engine)