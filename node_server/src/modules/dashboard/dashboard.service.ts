export class DashboardService {
    public static async getDashboardData() {
        return {
            kpis: {
                totalDecisions: 124,
                pendingApprovals: 3,
                negotiationSuccessRate: 98.4,
                activeAgents: 4,
            },
            recentDecisions: [
                {
                    id: 'dec_101',
                    title: 'Q3 Inventory Rebalancing & Marketing Promotion',
                    status: 'APPROVED',
                    timestamp: new Date().toISOString(),
                },
                {
                    id: 'dec_102',
                    title: 'Logistics Expedition & Budget Overrun Waiver',
                    status: 'PENDING_APPROVAL',
                    timestamp: new Date().toISOString(),
                },
            ],
            alerts: [
                {
                    id: 'alt_01',
                    severity: 'WARNING',
                    message: 'Sales forecast exceeds current inventory stock in Western Region.',
                    timestamp: new Date().toISOString(),
                },
            ],
        };
    }
}
