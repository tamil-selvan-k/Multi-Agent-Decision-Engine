import { z } from 'zod';
import { ApprovalService } from './approval.service';
import { asyncHandler } from '@utils/asyncHandler';
import { ApiResponse } from '@utils/ApiResponse';
import { AppError } from '@utils/AppError';
import { AuthenticatedRequest } from '@appTypes/auth.types';

const approvalSchema = z.object({
    action: z.enum(['approve', 'reject']),
});

export class ApprovalController {
    public static handleApproval = asyncHandler(async (req: AuthenticatedRequest) => {
        const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
        const parseResult = approvalSchema.safeParse(req.body);
        if (!parseResult.success) {
            throw new AppError("Invalid payload. 'action' must be 'approve' or 'reject'", 400, parseResult.error.issues);
        }

        const userId = req.user?.userId || 'unknown';
        const result = await ApprovalService.processApproval(id, parseResult.data.action, userId);
        return new ApiResponse(200, result, `Decision ${result.status.toLowerCase()} successfully`);
    });
}
