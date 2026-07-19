import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { OAuth2Client } from 'google-auth-library';
import { prisma } from '@utils/prisma';
import { config } from '@config/index';

const googleClient = new OAuth2Client(config.google.clientId);

export interface JwtPayload {
    userId: string;
    email: string;
    role: string;
    permissions: string[];
}

export class AuthService {
    /**
     * Helper to format permissions array from Role model
     */
    private static extractPermissions(rolePermissions: { permission: { name: string } }[]): string[] {
        return rolePermissions.map((rp) => rp.permission.name);
    }

    /**
     * Generate JWT for authenticated user
     */
    public static generateToken(payload: JwtPayload): string {
        return jwt.sign(payload, config.jwt.secret, {
            expiresIn: config.jwt.expiresIn as jwt.SignOptions['expiresIn'],
        });
    }

    /**
     * Register a new user with Email and Password
     */
    public static async register(data: { email: string; password: string; name: string; roleName?: string }) {
        const existingUser = await prisma.user.findUnique({
            where: { email: data.email },
        });

        if (existingUser) {
            throw new Error('User with this email already exists');
        }

        const targetRoleName = data.roleName || 'Employee';
        const role = await prisma.role.findUnique({
            where: { name: targetRoleName },
            include: { permissions: { include: { permission: true } } },
        });

        if (!role) {
            throw new Error(`Role '${targetRoleName}' not found`);
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

    /**
     * Authenticate user with Email and Password
     */
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
            throw new Error('Invalid email or password');
        }

        const isValidPassword = await bcrypt.compare(data.password, user.passwordHash);
        if (!isValidPassword) {
            throw new Error('Invalid email or password');
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

    /**
     * Authenticate or register user via Google OAuth ID Token
     */
    public static async loginWithGoogle(idToken: string) {
        let googlePayload;
        try {
            const ticket = await googleClient.verifyIdToken({
                idToken,
                audience: config.google.clientId,
            });
            googlePayload = ticket.getPayload();
        } catch (error) {
            throw new Error('Invalid Google ID token');
        }

        if (!googlePayload || !googlePayload.email) {
            throw new Error('Google token payload incomplete');
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
            // Find default Employee role
            const defaultRole = await prisma.role.findUnique({
                where: { name: 'Employee' },
                include: { permissions: { include: { permission: true } } },
            });

            if (!defaultRole) {
                throw new Error('Default Employee role is missing in system');
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
            // Link existing account with Google ID
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

    /**
     * Get user profile by ID
     */
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
            throw new Error('User not found');
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
