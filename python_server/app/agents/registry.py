from agents.inventory_agent import inventory_agent
from agents.logistics_agent import logistics_agent
from agents.sales_agent import sales_agent
from agents.finance_agent import finance_agent


AGENT_REGISTRY = {
    "InventoryAgent": inventory_agent,
    "LogisticsAgent": logistics_agent,
    "SalesAgent": sales_agent,
    "FinanceAgent": finance_agent,
}