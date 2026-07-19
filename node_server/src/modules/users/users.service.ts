import { UserRepository } from './users.repository';
import { AppError } from '@utils/AppError';

export class UserService {
    public static async getProfile(userId: string) {
        const user = await UserRepository.findById(userId);
        if (!user) {
            throw new AppError('User not found', 404);
        }

        const permissions = user.role.permissions.map((p) => p.permission.name);
        return {
            id: user.id,
            email: user.email,
            name: user.name,
            role: user.role.name,
            permissions,
            createdAt: user.createdAt,
            updatedAt: user.updatedAt,
        };
    }

    public static async getAllUsers() {
        return UserRepository.findAll();
    }

    public static async getUserById(id: string) {
        const user = await UserRepository.findById(id);
        if (!user) {
            throw new AppError(`User with ID '${id}' not found`, 404);
        }

        const permissions = user.role.permissions.map((p) => p.permission.name);
        return {
            id: user.id,
            email: user.email,
            name: user.name,
            role: user.role.name,
            permissions,
            createdAt: user.createdAt,
        };
    }

    public static async updateUser(id: string, data: { name?: string; roleName?: string }) {
        const user = await UserRepository.findById(id);
        if (!user) {
            throw new AppError(`User with ID '${id}' not found`, 404);
        }

        let roleId: string | undefined;
        if (data.roleName) {
            const role = await UserRepository.findRoleByName(data.roleName);
            if (!role) {
                throw new AppError(`Role '${data.roleName}' not found`, 404);
            }
            roleId = role.id;
        }

        return UserRepository.updateUser(id, {
            name: data.name,
            roleId,
        });
    }
}
