import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { OAuth2Client } from 'google-auth-library';
import { prisma } from '@utils/prisma';
import { config } from '@config/index';
import { JwtPayload } from '@appTypes/auth.types';
import { RoleEnum } from '@appTypes/rbac.enum';
import { AppError } from '@utils/AppError';

const googleClient = new OAuth2Client(config.google.clientId);

export class AuthService {
    private static extractPermissions(rolePermissions: { permission: { name: string } }[]): string[] {
        return rolePermissions.map((rp) => rp.permission.name);
    }

    public static generateToken(payload: JwtPayload): string {
        return jwt.sign(payload, config.jwt.secret, {
            expiresIn: config.jwt.expiresIn as jwt.SignOptions['expiresIn'],
        });
    }

    public static async register(data: { email: string; password: string; name: string; roleName?: string }) {
        const existingUser = await prisma.user.findUnique({
            where: { email: data.email },
        });

        if (existingUser) {
            throw new AppError('User with this email already exists', 409);
        }

        const targetRoleName = data.roleName || RoleEnum.EXECUTIVE;
        const role = await prisma.role.findUnique({
            where: { name: targetRoleName },
            include: { permissions: { include: { permission: true } } },
        });

        if (!role) {
            throw new AppError(`Role '${targetRoleName}' not found`, 404);
        }

        const passwordHash = await bcrypt.hash(data.password, 10);

        const user = await prisma.user.create({
            data: {
                email: data.email,
                name: data.name,
                passwordHash,
                roleId: role.id,
            },
            include: {
                role: {
                    include: {
                        permissions: {
                            include: { permission: true },
                        },
                    },
                },
            },
        });

        const permissions = this.extractPermissions(user.role.permissions);
        const token = this.generateToken({
            userId: user.id,
            email: user.email,
            role: user.role.name,
            permissions,
        });

        return {
            token,
            user: {
                id: user.id,
                email: user.email,
                name: user.name,
                role: user.role.name,
                permissions,
            },
        };
    }

    public static async login(data: { email: string; password: string }) {
        const user = await prisma.user.findUnique({
            where: { email: data.email },
            include: {
                role: {
                    include: {
                        permissions: {
                            include: { permission: true },
                        },
                    },
                },
            },
        });

        if (!user || !user.passwordHash) {
            throw new AppError('Invalid email or password', 401);
        }

        const isValidPassword = await bcrypt.compare(data.password, user.passwordHash);
        if (!isValidPassword) {
            throw new AppError('Invalid email or password', 401);
        }

        const permissions = this.extractPermissions(user.role.permissions);
        const token = this.generateToken({
            userId: user.id,
            email: user.email,
            role: user.role.name,
            permissions,
        });

        return {
            token,
            user: {
                id: user.id,
                email: user.email,
                name: user.name,
                role: user.role.name,
                permissions,
            },
        };
    }

    public static async loginWithGoogle(idToken: string) {
        let googlePayload;
        try {
            const ticket = await googleClient.verifyIdToken({
                idToken,
                audience: config.google.clientId,
            });
            googlePayload = ticket.getPayload();
        } catch (error) {
            throw new AppError('Invalid Google ID token', 401);
        }

        if (!googlePayload || !googlePayload.email) {
            throw new AppError('Google token payload incomplete', 400);
        }

        const { email, sub: googleId, name } = googlePayload;

        let user = await prisma.user.findUnique({
            where: { email },
            include: {
                role: {
                    include: {
                        permissions: {
                            include: { permission: true },
                        },
                    },
                },
            },
        });

        if (!user) {
            const defaultRole = await prisma.role.findUnique({
                where: { name: RoleEnum.EXECUTIVE },
                include: { permissions: { include: { permission: true } } },
            });

            if (!defaultRole) {
                throw new AppError('Default Executive role is missing in system', 500);
            }

            user = await prisma.user.create({
                data: {
                    email,
                    name: name || 'Google User',
                    googleId,
                    roleId: defaultRole.id,
                },
                include: {
                    role: {
                        include: {
                            permissions: {
                                include: { permission: true },
                            },
                        },
                    },
                },
            });
        } else if (!user.googleId) {
            user = await prisma.user.update({
                where: { id: user.id },
                data: { googleId },
                include: {
                    role: {
                        include: {
                            permissions: {
                                include: { permission: true },
                            },
                        },
                    },
                },
            });
        }

        const permissions = this.extractPermissions(user.role.permissions);
        const token = this.generateToken({
            userId: user.id,
            email: user.email,
            role: user.role.name,
            permissions,
        });

        return {
            token,
            user: {
                id: user.id,
                email: user.email,
                name: user.name,
                role: user.role.name,
                permissions,
            },
        };
    }

    public static async getProfile(userId: string) {
        const user = await prisma.user.findUnique({
            where: { id: userId },
            include: {
                role: {
                    include: {
                        permissions: {
                            include: { permission: true },
                        },
                    },
                },
            },
        });

        if (!user) {
            throw new AppError('User not found', 404);
        }

        const permissions = this.extractPermissions(user.role.permissions);
        return {
            id: user.id,
            email: user.email,
            name: user.name,
            role: user.role.name,
            permissions,
            createdAt: user.createdAt,
        };
    }
}
