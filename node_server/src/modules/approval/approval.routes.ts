import { Router } from 'express';
import { ApprovalController } from './approval.controller';
import { authenticateJWT, requirePermission } from '@middleware/auth.middleware';
import { PermissionEnum } from '@appTypes/rbac.enum';

const router = Router();

router.use(authenticateJWT);
router.post('/:id', requirePermission(PermissionEnum.APPROVE_DECISION), ApprovalController.handleApproval);

export default router;
