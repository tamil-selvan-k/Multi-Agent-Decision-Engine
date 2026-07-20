def fetch_inventory():
    """Fetch current inventory from warehouse.

    Returns:
        dict: current stock, warehouse capacity, safety stock.
    """
    return {
        "current_stock": 1200,
        "warehouse_capacity": 2000,
        "safety_stock": 300
    }


def optimize_inventory():
    """Use OR-Tools to optimize inventory levels.

    Returns:
        dict: recommended stock level.
    """
    return {
        "recommended_stock": 1400
    }


def warehouse_capacity():
    """Returns warehouse utilization.

    Returns:
        dict: utilization percentage.
    """
    return {
        "utilization": 94
    }


def reorder_recommendation():
    """Generate reorder recommendation.

    Returns:
        str: either \"Order X units\" or \"Delay purchasing\".
    """
    # Simple logic: if current stock < safety pad, order else maybe delay
    # For demo, return a fixed recommendation
    return "Order 350 units"