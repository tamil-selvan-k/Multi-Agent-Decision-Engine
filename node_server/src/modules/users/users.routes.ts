import { Router } from 'express';
import { UserController } from './users.controller';
import { authenticateJWT, requirePermission } from '@middleware/auth.middleware';
import { PermissionEnum } from '@appTypes/rbac.enum';

const router = Router();

router.use(authenticateJWT);

router.get('/me', UserController.getMe);
router.get('/', requirePermission(PermissionEnum.MANAGE_USERS), UserController.getUsers);
router.get('/:id', requirePermission(PermissionEnum.MANAGE_USERS), UserController.getUserById);
router.patch('/:id', requirePermission(PermissionEnum.MANAGE_USERS), UserController.updateUser);

export default router;
