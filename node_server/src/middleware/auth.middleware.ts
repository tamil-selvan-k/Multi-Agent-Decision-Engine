import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '@config/index';
import { JwtPayload } from '@modules/auth/auth.service';

export interface AuthenticatedRequest extends Request {
    user?: JwtPayload;
}

/**
 * Middleware to verify JWT token from Authorization header
 */
export const authenticateJWT = (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        res.status(401).json({
            success: false,
            message: 'Access token missing or invalid format. Header format: Bearer <token>',
        });
        return;
    }

    const token = authHeader.split(' ')[1];

    try {
        const decoded = jwt.verify(token, config.jwt.secret) as JwtPayload;
        req.user = decoded;
        next();
    } catch (error) {
        res.status(401).json({
            success: false,
            message: 'Invalid or expired access token',
        });
        return;
    }
};

/**
 * Role-Based Access Control Middleware (RBAC)
 * @param roles Array of allowed role names (e.g. ['Admin', 'Manager'])
 */
export const requireRole = (...roles: string[]) => {
    return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
        if (!req.user) {
            res.status(401).json({ success: false, message: 'Authentication required' });
            return;
        }

        if (!roles.includes(req.user.role)) {
            res.status(403).json({
                success: false,
                message: `Forbidden: Requires one of roles [${roles.join(', ')}]. Current role: '${req.user.role}'`,
            });
            return;
        }

        next();
    };
};

/**
 * Permission-Based Access Control Middleware
 * @param requiredPermissions Array of required permission names (e.g. ['view_reports', 'approve_orders'])
 */
export const requirePermission = (...requiredPermissions: string[]) => {
    return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
        if (!req.user) {
            res.status(401).json({ success: false, message: 'Authentication required' });
            return;
        }

        const userPermissions = req.user.permissions || [];
        const hasAllPermissions = requiredPermissions.every((perm) => userPermissions.includes(perm));

        if (!hasAllPermissions) {
            res.status(403).json({
                success: false,
                message: `Forbidden: Missing required permissions [${requiredPermissions.join(', ')}]`,
            });
            return;
        }

        next();
    };
};
