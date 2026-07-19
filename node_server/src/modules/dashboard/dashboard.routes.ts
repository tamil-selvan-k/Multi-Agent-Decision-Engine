import { Router } from 'express';
import { DashboardController } from './dashboard.controller';
import { authenticateJWT, requirePermission } from '@middleware/auth.middleware';
import { PermissionEnum } from '@appTypes/rbac.enum';

const router = Router();

router.use(authenticateJWT);
router.get('/', requirePermission(PermissionEnum.VIEW_DASHBOARD), DashboardController.getDashboard);

export default router;
