import { AppError } from '@utils/AppError';

export class DecisionService {
    public static async runDecisionCycle(parameters?: Record<string, any>) {
        const sessionId = `session_${Date.now()}`;
        const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:3001/api/v1/orchestrate';

        const response = await fetch(pythonServiceUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                parameters: parameters || {},
            }),
        });

        const data: any = await response.json();

        if (!response.ok) {
            throw new AppError(
                data.message || 'Failed to communicate with Python AI Orchestration service',
                response.status,
                data.errors || []
            );
        }

        return data;
    }

    public static async getDecisionHistory() {
        return [
            {
                id: 'dec_101',
                status: 'APPROVED',
                summary: 'Optimized sales allocation with 15% inventory buffer.',
                agentsInvolved: ['SalesAgent', 'InventoryAgent', 'FinanceAgent'],
                createdAt: new Date(Date.now() - 3600000).toISOString(),
            },
            {
                id: 'dec_100',
                status: 'COMPLETED',
                summary: 'Budget shift approved for expedited freight.',
                agentsInvolved: ['LogisticsAgent', 'FinanceAgent'],
                createdAt: new Date(Date.now() - 86400000).toISOString(),
            },
        ];
    }

    public static async getDecisionById(id: string) {
        if (!id) {
            throw new AppError('Decision ID is required', 400);
        }
        return {
            id,
            status: 'processing',
            details: {
                target: 'Enterprise Supply Chain & Demand Alignment',
                agents: {
                    sales: { recommendation: 'Increase promo spend by 10%', confidence: 0.92 },
                    inventory: { recommendation: 'Reorder 500 units from Supplier A', confidence: 0.88 },
                    finance: { recommendation: 'Approve $5,000 budget reallocation', confidence: 0.95 },
                },
            },
            createdAt: new Date().toISOString(),
        };
    }
}
