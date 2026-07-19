import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { AuthService } from './auth.service';

const registerSchema = z.object({
    email: z.string().email(),
    password: z.string().min(6),
    name: z.string().min(2),
    roleName: z.enum(['Admin', 'Manager', 'Employee']).optional(),
});

const loginSchema = z.object({
    email: z.string().email(),
    password: z.string(),
});

const googleAuthSchema = z.object({
    idToken: z.string().min(1, 'Google ID token is required'),
});

export class AuthController {
    public static async register(req: Request, res: Response, next: NextFunction) {
        try {
            const body = registerSchema.parse(req.body);
            const result = await AuthService.register(body);
            res.status(201).json({
                success: true,
                message: 'User registered successfully',
                data: result,
            });
        } catch (error: any) {
            next(error);
        }
    }

    public static async login(req: Request, res: Response, next: NextFunction) {
        try {
            const body = loginSchema.parse(req.body);
            const result = await AuthService.login(body);
            res.status(200).json({
                success: true,
                message: 'Login successful',
                data: result,
            });
        } catch (error: any) {
            next(error);
        }
    }

    public static async googleLogin(req: Request, res: Response, next: NextFunction) {
        try {
            const { idToken } = googleAuthSchema.parse(req.body);
            const result = await AuthService.loginWithGoogle(idToken);
            res.status(200).json({
                success: true,
                message: 'Google authentication successful',
                data: result,
            });
        } catch (error: any) {
            next(error);
        }
    }

    public static async getMe(req: Request, res: Response, next: NextFunction) {
        try {
            const userPayload = (req as any).user;
            if (!userPayload || !userPayload.userId) {
                res.status(401).json({ success: false, message: 'Unauthorized' });
                return;
            }
            const profile = await AuthService.getProfile(userPayload.userId);
            res.status(200).json({
                success: true,
                data: profile,
            });
        } catch (error: any) {
            next(error);
        }
    }
}
