export type Role = 'Admin' | 'Manager' | 'Analyst' | 'Executive';

export interface User {
  id: string;
  email: string;
  name: string;
  role: Role;
  permissions: string[];
}

export interface AgentMetric {
  agent_name: string;
  recommendation: string;
  confidence: number;
  metrics: Record<string, any>;
}

export interface EnterpriseDecisionData {
  session_id: string;
  status: string;
  final_decision: string;
  agent_outputs: AgentMetric[];
  merged_at: string;
}

export interface DashboardData {
  kpis: {
    totalDecisions: number;
    pendingApprovals: number;
    negotiationSuccessRate: number;
    activeAgents: number;
  };
  recentDecisions: Array<{
    id: string;
    title: string;
    status: string;
    timestamp: string;
  }>;
  alerts: Array<{
    id: string;
    severity: string;
    message: string;
    timestamp: string;
  }>;
}

export interface SimulationResult {
  scenarioInput: {
    demandIncreasePercent: number;
    budgetReductionPercent: number;
  };
  simulationResults: {
    projectedRevenueImpactPercent: number;
    projectedInventoryStockoutRisk: string;
    recommendedReallocation: {
      expeditedFreightBudget: string;
      bufferStockUnits: number;
    };
    agentsConsensus: string;
  };
  timestamp: string;
}
