from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import models

def fetch_shipments():
    """Fetch current shipments.

    Returns:
        list: list of dicts with shipment info.
    """
    db = SessionLocal()
    try:
        shipment_records = db.query(models.Shipment).all()
        if not shipment_records:
            # Insert default data as per spec
            default_data = [
    {
        "shipment_id": "SHIP001",
        "order_id": "ORD001",
        "supplier_id": "SUP001",
        "supplier_name": "ABC Suppliers",
        "warehouse_id": "WH001",
        "origin": "Chennai",
        "destination": "Bangalore",
        "vehicle_type": "Truck",
        "distance_km": 350,
        "dispatch_date": "2026-07-20",
        "eta": 10,
        "actual_delivery_date": None,
        "transportation_cost": 6500,
        "status": "In Transit",
        "delay_hours": 1,
        "lead_time": 2,
        "supplier_reliability": 0.95,
        "quality_score": 0.97,
        "on_time_delivery": 0.94,
        "available_stock": 180
    },
    {
        "shipment_id": "SHIP002",
        "order_id": "ORD002",
        "supplier_id": "SUP002",
        "supplier_name": "Global Logistics",
        "warehouse_id": "WH002",
        "origin": "Mumbai",
        "destination": "Hyderabad",
        "vehicle_type": "Van",
        "distance_km": 710,
        "dispatch_date": "2026-07-19",
        "eta": 18,
        "actual_delivery_date": "2026-07-20",
        "transportation_cost": 9800,
        "status": "Delivered",
        "delay_hours": 0,
        "lead_time": 3,
        "supplier_reliability": 0.92,
        "quality_score": 0.95,
        "on_time_delivery": 0.96,
        "available_stock": 90
    },
    {
        "shipment_id": "SHIP003",
        "order_id": "ORD003",
        "supplier_id": "SUP003",
        "supplier_name": "Prime Supply",
        "warehouse_id": "WH001",
        "origin": "Chennai",
        "destination": "Coimbatore",
        "vehicle_type": "Truck",
        "distance_km": 510,
        "dispatch_date": "2026-07-18",
        "eta": 14,
        "actual_delivery_date": None,
        "transportation_cost": 7200,
        "status": "Delayed",
        "delay_hours": 4,
        "lead_time": 2,
        "supplier_reliability": 0.83,
        "quality_score": 0.90,
        "on_time_delivery": 0.82,
        "available_stock": 150
    },
    {
        "shipment_id": "SHIP004",
        "order_id": "ORD004",
        "supplier_id": "SUP001",
        "supplier_name": "ABC Suppliers",
        "warehouse_id": "WH003",
        "origin": "Delhi",
        "destination": "Jaipur",
        "vehicle_type": "Mini Truck",
        "distance_km": 280,
        "dispatch_date": "2026-07-21",
        "eta": 8,
        "actual_delivery_date": None,
        "transportation_cost": 4200,
        "status": "In Transit",
        "delay_hours": 0,
        "lead_time": 1,
        "supplier_reliability": 0.97,
        "quality_score": 0.98,
        "on_time_delivery": 0.99,
        "available_stock": 300
    },
    {
        "shipment_id": "SHIP005",
        "order_id": "ORD005",
        "supplier_id": "SUP002",
        "supplier_name": "Global Logistics",
        "warehouse_id": "WH002",
        "origin": "Pune",
        "destination": "Nagpur",
        "vehicle_type": "Truck",
        "distance_km": 690,
        "dispatch_date": "2026-07-17",
        "eta": 20,
        "actual_delivery_date": "2026-07-18",
        "transportation_cost": 10500,
        "status": "Delivered",
        "delay_hours": 2,
        "lead_time": 3,
        "supplier_reliability": 0.88,
        "quality_score": 0.91,
        "on_time_delivery": 0.86,
        "available_stock": 70
    },
    {
        "shipment_id": "SHIP006",
        "order_id": "ORD006",
        "supplier_id": "SUP003",
        "supplier_name": "Prime Supply",
        "warehouse_id": "WH003",
        "origin": "Kolkata",
        "destination": "Bhubaneswar",
        "vehicle_type": "Van",
        "distance_km": 440,
        "dispatch_date": "2026-07-22",
        "eta": 12,
        "actual_delivery_date": None,
        "transportation_cost": 5600,
        "status": "In Transit",
        "delay_hours": 1,
        "lead_time": 2,
        "supplier_reliability": 0.90,
        "quality_score": 0.93,
        "on_time_delivery": 0.91,
        "available_stock": 220
    },
    {
        "shipment_id": "SHIP007",
        "order_id": "ORD007",
        "supplier_id": "SUP001",
        "supplier_name": "ABC Suppliers",
        "warehouse_id": "WH001",
        "origin": "Chennai",
        "destination": "Madurai",
        "vehicle_type": "Truck",
        "distance_km": 460,
        "dispatch_date": "2026-07-23",
        "eta": 11,
        "actual_delivery_date": None,
        "transportation_cost": 6100,
        "status": "In Transit",
        "delay_hours": 0,
        "lead_time": 2,
        "supplier_reliability": 0.96,
        "quality_score": 0.98,
        "on_time_delivery": 0.97,
        "available_stock": 210
    },
    {
        "shipment_id": "SHIP008",
        "order_id": "ORD008",
        "supplier_id": "SUP002",
        "supplier_name": "Global Logistics",
        "warehouse_id": "WH002",
        "origin": "Ahmedabad",
        "destination": "Surat",
        "vehicle_type": "Mini Truck",
        "distance_km": 270,
        "dispatch_date": "2026-07-20",
        "eta": 7,
        "actual_delivery_date": "2026-07-20",
        "transportation_cost": 3900,
        "status": "Delivered",
        "delay_hours": 0,
        "lead_time": 1,
        "supplier_reliability": 0.98,
        "quality_score": 0.99,
        "on_time_delivery": 0.99,
        "available_stock": 130
    }
]
            for item in default_data:
                db.add(models.Shipment(**item))
            db.commit()
            shipment_records = db.query(models.Shipment).all()
        # Convert to list of dicts
        result = [
    {
        "shipment_id": record.shipment_id,
        "order_id": record.order_id,
        "supplier_id": record.supplier_id,
        "supplier_name": record.supplier_name,
        "warehouse_id": record.warehouse_id,
        "origin": record.origin,
        "destination": record.destination,
        "vehicle_type": record.vehicle_type,
        "distance_km": record.distance_km,
        "dispatch_date": record.dispatch_date,
        "eta": record.eta,
        "actual_delivery_date": record.actual_delivery_date,
        "transportation_cost": record.transportation_cost,
        "status": record.status,
        "delay_hours": record.delay_hours,
        "lead_time": record.lead_time,
        "supplier_reliability": record.supplier_reliability,
        "quality_score": record.quality_score,
        "on_time_delivery": record.on_time_delivery,
        "available_stock": record.available_stock
    }
    for record in shipment_records
]
        return result
    finally:
        db.close()

def optimize_routes():
    """Optimize delivery routes based on shortest total distance.

    Returns:
        dict: best route and total distance.
    """
    db = SessionLocal()
    try:
        shipment_records = db.query(models.Shipment).all()

        if not shipment_records:
            return {
                "best_route": [],
                "total_distance_km": 0,
                "reason": "No shipment data available."
            }

        # Sort shipments by distance
        sorted_shipments = sorted(
            shipment_records,
            key=lambda shipment: shipment.distance_km or 0
        )

        best_route = []
        total_distance = 0

        for shipment in sorted_shipments:
            best_route.append(
                f"{shipment.origin} → {shipment.destination}"
            )
            total_distance += shipment.distance_km or 0

        route_record = db.query(models.RouteOptimization).first()

        if route_record:
            route_record.best_route = ",".join(best_route)
            route_record.total_distance_km = round(total_distance, 2)
        else:
            route_record = models.RouteOptimization(
                best_route=",".join(best_route),
                total_distance_km=round(total_distance, 2)
            )
            db.add(route_record)

        db.commit()

        return {
            "best_route": best_route,
            "total_distance_km": round(total_distance, 2),
            "reason": "Routes ordered by shortest delivery distance."
        }

    finally:
        db.close()

def delivery_eta():
    """Estimate average delivery time and delay probability.

    Returns:
        dict: estimated delivery hours and delay probability.
    """
    db = SessionLocal()
    try:
        shipment_records = db.query(models.Shipment).all()

        if not shipment_records:
            return {
                "estimated_delivery_hours": 0,
                "delay_probability": 0.0,
                "reason": "No shipment data available."
            }

        total_eta = 0
        delayed_shipments = 0

        for shipment in shipment_records:
            eta = shipment.eta or 0
            total_eta += eta

            if (shipment.delay_hours or 0) > 0:
                delayed_shipments += 1

        estimated_delivery_hours = round(
            total_eta / len(shipment_records), 2
        )

        delay_probability = round(
            delayed_shipments / len(shipment_records), 2
        )

        eta_record = db.query(models.DeliveryETA).first()

        if eta_record:
            eta_record.estimated_delivery_hours = estimated_delivery_hours
            eta_record.delay_probability = delay_probability
        else:
            eta_record = models.DeliveryETA(
                estimated_delivery_hours=estimated_delivery_hours,
                delay_probability=delay_probability
            )
            db.add(eta_record)

        db.commit()

        return {
            "estimated_delivery_hours": estimated_delivery_hours,
            "delay_probability": delay_probability,
            "reason": "Calculated from current shipment ETA and delays."
        }

    finally:
        db.close()

def warehouse_assignment():
    """Assign shipments to the most suitable warehouse.

    Returns:
        dict: recommended warehouse with available stock.
    """
    db = SessionLocal()
    try:
        shipment_records = db.query(models.Shipment).all()

        if not shipment_records:
            return {
                "recommended_warehouse": None,
                "available_stock": 0,
                "reason": "No shipment data available."
            }

        warehouse_stock = {}

        for shipment in shipment_records:
            warehouse = shipment.warehouse_id

            if warehouse not in warehouse_stock:
                warehouse_stock[warehouse] = 0

            warehouse_stock[warehouse] += shipment.available_stock or 0

        recommended_warehouse = max(
            warehouse_stock,
            key=warehouse_stock.get
        )

        recommendation = db.query(models.WarehouseAssignment).first()

        if recommendation:
            recommendation.recommended_warehouse = recommended_warehouse
        else:
            recommendation = models.WarehouseAssignment(
                recommended_warehouse=recommended_warehouse
            )
            db.add(recommendation)

        db.commit()

        return {
            "recommended_warehouse": recommended_warehouse,
            "available_stock": warehouse_stock[recommended_warehouse],
            "reason": "Warehouse has the highest available stock."
        }

    finally:
        db.close()

def calculate_transport_cost():
    """Calculate transportation cost statistics.

    Returns:
        dict: transport cost summary.
    """
    db = SessionLocal()
    try:
        shipment_records = db.query(models.Shipment).all()

        if not shipment_records:
            return {
                "total_transport_cost": 0,
                "average_transport_cost": 0,
                "highest_transport_cost": 0,
                "lowest_transport_cost": 0,
                "reason": "No shipment data available."
            }

        costs = [
            shipment.transportation_cost
            for shipment in shipment_records
            if shipment.transportation_cost is not None
        ]

        if not costs:
            return {
                "total_transport_cost": 0,
                "average_transport_cost": 0,
                "highest_transport_cost": 0,
                "lowest_transport_cost": 0,
                "reason": "Transportation cost data unavailable."
            }

        total_cost = sum(costs)
        average_cost = total_cost / len(costs)

        return {
            "total_transport_cost": round(total_cost, 2),
            "average_transport_cost": round(average_cost, 2),
            "highest_transport_cost": round(max(costs), 2),
            "lowest_transport_cost": round(min(costs), 2),
            "reason": "Calculated from all shipment transportation costs."
        }

    finally:
        db.close()

def delivery_risk_analysis():
    """Analyze logistics delivery risk.

    Returns:
        dict: risk score, level and reason.
    """
    db = SessionLocal()
    try:
        shipment_records = db.query(models.Shipment).all()

        if not shipment_records:
            return {
                "risk_score": 0,
                "risk_level": "Unknown",
                "reason": "No shipment data available."
            }

        total_score = 0

        for shipment in shipment_records:
            score = 0

            # Delay contribution
            if shipment.delay_hours:
                score += min(shipment.delay_hours * 2, 30)

            # Supplier reliability contribution
            if shipment.supplier_reliability is not None:
                score += (1 - shipment.supplier_reliability) * 30

            # On-time delivery contribution
            if shipment.on_time_delivery is not None:
                score += (1 - shipment.on_time_delivery) * 20

            # Quality contribution
            if shipment.quality_score is not None:
                score += (1 - shipment.quality_score) * 20

            total_score += score

        risk_score = round(total_score / len(shipment_records), 2)

        if risk_score < 30:
            risk_level = "Low"
        elif risk_score < 60:
            risk_level = "Medium"
        else:
            risk_level = "High"

        reason = f"Calculated from delivery delays, supplier reliability, on-time delivery and quality scores."

        risk_record = db.query(models.DeliveryRisk).first()

        if risk_record:
            risk_record.risk_score = risk_score
            risk_record.risk_level = risk_level
            risk_record.reason = reason
        else:
            risk_record = models.DeliveryRisk(
                risk_score=risk_score,
                risk_level=risk_level,
                reason=reason
            )
            db.add(risk_record)

        db.commit()

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reason": reason
        }

    finally:
        db.close()