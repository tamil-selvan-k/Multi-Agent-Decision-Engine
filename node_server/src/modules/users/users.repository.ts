import { prisma } from '@utils/prisma';

export class UserRepository {
    public static async findById(id: string) {
        return prisma.user.findUnique({
            where: { id },
            select: {
                id: true,
                email: true,
                name: true,
                roleId: true,
                createdAt: true,
                updatedAt: true,
                role: {
                    select: {
                        id: true,
                        name: true,
                        permissions: {
                            select: {
                                permission: {
                                    select: { name: true },
                                },
                            },
                        },
                    },
                },
            },
        });
    }

    public static async findAll() {
        return prisma.user.findMany({
            select: {
                id: true,
                email: true,
                name: true,
                createdAt: true,
                role: {
                    select: {
                        name: true,
                    },
                },
            },
            orderBy: { createdAt: 'desc' },
        });
    }

    public static async updateUser(id: string, data: { name?: string; roleId?: string }) {
        return prisma.user.update({
            where: { id },
            data,
            select: {
                id: true,
                email: true,
                name: true,
                role: {
                    select: {
                        name: true,
                    },
                },
                updatedAt: true,
            },
        });
    }

    public static async findRoleByName(roleName: string) {
        return prisma.role.findUnique({
            where: { name: roleName },
        });
    }
}
