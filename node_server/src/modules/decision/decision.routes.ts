import { Router } from 'express';
import { DecisionController } from './decision.controller';
import { authenticateJWT, requirePermission } from '@middleware/auth.middleware';
import { PermissionEnum } from '@appTypes/rbac.enum';

const router = Router();

router.use(authenticateJWT);

router.post('/run', requirePermission(PermissionEnum.RUN_DECISION), DecisionController.runDecision);
router.get('/history', requirePermission(PermissionEnum.RUN_DECISION), DecisionController.getHistory);
router.get('/:id', requirePermission(PermissionEnum.RUN_DECISION), DecisionController.getDecisionById);

export default router;
