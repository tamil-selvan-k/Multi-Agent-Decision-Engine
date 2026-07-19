import { AppError } from '@utils/AppError';

export class ApprovalService {
    public static async processApproval(decisionId: string, action: string, userId: string) {
        if (!['approve', 'reject'].includes(action.toLowerCase())) {
            throw new AppError("Invalid action. Must be 'approve' or 'reject'", 400);
        }

        return {
            decisionId,
            action: action.toLowerCase(),
            status: action.toLowerCase() === 'approve' ? 'APPROVED' : 'REJECTED',
            processedBy: userId,
            timestamp: new Date().toISOString(),
        };
    }
}
