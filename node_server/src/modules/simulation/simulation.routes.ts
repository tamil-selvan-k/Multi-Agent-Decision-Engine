import { Router } from 'express';
import { SimulationController } from './simulation.controller';
import { authenticateJWT, requirePermission } from '@middleware/auth.middleware';
import { PermissionEnum } from '@appTypes/rbac.enum';

const router = Router();

router.use(authenticateJWT);
router.post('/', requirePermission(PermissionEnum.RUN_SIMULATION), SimulationController.runSimulation);

export default router;
