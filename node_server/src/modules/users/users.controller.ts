import { Request } from 'express';
import { z } from 'zod';
import { UserService } from './users.service';
import { asyncHandler } from '@utils/asyncHandler';
import { ApiResponse } from '@utils/ApiResponse';
import { AppError } from '@utils/AppError';
import { AuthenticatedRequest } from '@appTypes/auth.types';
import { RoleEnum } from '@appTypes/rbac.enum';

const updateUserSchema = z.object({
    name: z.string().min(2).optional(),
    roleName: z.nativeEnum(RoleEnum).optional(),
});

export class UserController {
    public static getMe = asyncHandler(async (req: AuthenticatedRequest) => {
        if (!req.user?.userId) {
            throw new AppError('Unauthorized access', 401);
        }
        const profile = await UserService.getProfile(req.user.userId);
        return new ApiResponse(200, profile, 'Profile fetched successfully');
    });

    public static getUsers = asyncHandler(async () => {
        const users = await UserService.getAllUsers();
        return new ApiResponse(200, users, 'Users retrieved successfully');
    });

    public static getUserById = asyncHandler(async (req: Request) => {
        const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
        const user = await UserService.getUserById(id);
        return new ApiResponse(200, user, 'User details retrieved successfully');
    });

    public static updateUser = asyncHandler(async (req: Request) => {
        const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
        const parseResult = updateUserSchema.safeParse(req.body);
        if (!parseResult.success) {
            throw new AppError('Invalid update payload', 400, parseResult.error.issues);
        }
        const updatedUser = await UserService.updateUser(id, parseResult.data);
        return new ApiResponse(200, updatedUser, 'User updated successfully');
    });
}
