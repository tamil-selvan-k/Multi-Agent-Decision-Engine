import { Request, Response } from 'express';
import { z } from 'zod';
import { AuthService } from './auth.service';
import { asyncHandler } from '@utils/asyncHandler';
import { ApiResponse } from '@utils/ApiResponse';
import { AppError } from '@utils/AppError';
import { RoleEnum } from '@appTypes/rbac.enum';
import { AuthenticatedRequest } from '@appTypes/auth.types';

const registerSchema = z.object({
    email: z.string().email(),
    password: z.string().min(6),
    name: z.string().min(2),
    roleName: z.nativeEnum(RoleEnum).optional(),
});

const loginSchema = z.object({
    email: z.string().email(),
    password: z.string(),
});

const googleAuthSchema = z.object({
    idToken: z.string().min(1, 'Google ID token is required'),
});

export class AuthController {
    public static register = asyncHandler(async (req: Request) => {
        const parseResult = registerSchema.safeParse(req.body);
        if (!parseResult.success) {
            throw new AppError('Invalid registration data', 400, parseResult.error.issues);
        }
        const result = await AuthService.register(parseResult.data);
        return new ApiResponse(201, result, 'User registered successfully');
    });

    public static login = asyncHandler(async (req: Request) => {
        const parseResult = loginSchema.safeParse(req.body);
        if (!parseResult.success) {
            throw new AppError('Invalid login credentials payload', 400, parseResult.error.issues);
        }
        const result = await AuthService.login(parseResult.data);
        return new ApiResponse(200, result, 'Login successful');
    });

    public static googleLogin = asyncHandler(async (req: Request) => {
        const parseResult = googleAuthSchema.safeParse(req.body);
        if (!parseResult.success) {
            throw new AppError('Google ID token is missing or invalid', 400, parseResult.error.issues);
        }
        const result = await AuthService.loginWithGoogle(parseResult.data.idToken);
        return new ApiResponse(200, result, 'Google authentication successful');
    });

    public static getMe = asyncHandler(async (req: AuthenticatedRequest) => {
        const userPayload = req.user;
        if (!userPayload || !userPayload.userId) {
            throw new AppError('Unauthorized access', 401);
        }
        const profile = await AuthService.getProfile(userPayload.userId);
        return new ApiResponse(200, profile, 'User profile fetched successfully');
    });
}
