import { Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '@config/index';
import { JwtPayload, AuthenticatedRequest } from '@appTypes/auth.types';
import { RoleEnum, PermissionEnum } from '@appTypes/rbac.enum';
import { AppError } from '@utils/AppError';

export { AuthenticatedRequest };

/**
 * Middleware to verify JWT token from Authorization header
 */
export const authenticateJWT = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return next(new AppError('Access token missing or invalid format. Header format: Bearer <token>', 401));
    }

    const token = authHeader.split(' ')[1];

    try {
        const decoded = jwt.verify(token, config.jwt.secret) as JwtPayload;
        req.user = decoded;
        next();
    } catch (error) {
        return next(new AppError('Invalid or expired access token', 401));
    }
};

/**
 * Role-Based Access Control Middleware (RBAC)
 * @param roles Array of allowed role names or RoleEnum values
 */
export const requireRole = (...roles: (RoleEnum | string)[]) => {
    return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
        if (!req.user) {
            return next(new AppError('Authentication required', 401));
        }

        const allowedRoles = roles.map((r) => String(r));
        if (!allowedRoles.includes(req.user.role)) {
            return next(
                new AppError(
                    `Forbidden: Requires one of roles [${allowedRoles.join(', ')}]. Current role: '${req.user.role}'`,
                    403
                )
            );
        }

        next();
    };
};

/**
 * Permission-Based Access Control Middleware
 * @param requiredPermissions Array of required permission names or PermissionEnum values
 */
export const requirePermission = (...requiredPermissions: (PermissionEnum | string)[]) => {
    return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
        if (!req.user) {
            return next(new AppError('Authentication required', 401));
        }

        const userPermissions = req.user.permissions || [];
        const requiredPermStrings = requiredPermissions.map((p) => String(p));
        const hasAllPermissions = requiredPermStrings.every((perm) => userPermissions.includes(perm));

        if (!hasAllPermissions) {
            return next(
                new AppError(
                    `Forbidden: Missing required permissions [${requiredPermStrings.join(', ')}]`,
                    403
                )
            );
        }

        next();
    };
};
