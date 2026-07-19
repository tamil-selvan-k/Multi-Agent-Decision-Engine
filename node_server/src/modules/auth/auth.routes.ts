import { Router } from 'express';
import { AuthController } from './auth.controller';
import { authenticateJWT } from '@middleware/auth.middleware';

const router = Router();

// Public Auth routes
router.post('/register', AuthController.register);
router.post('/login', AuthController.login);
router.post('/google', AuthController.googleLogin);

// Protected Auth routes
router.get('/me', authenticateJWT, AuthController.getMe);

export default router;
