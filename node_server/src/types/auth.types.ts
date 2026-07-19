import { Request } from 'express';

export interface JwtPayload {
    userId: string;
    email: string;
    role: string;
    permissions: string[];
}

export interface AuthenticatedRequest extends Request {
    user?: JwtPayload;
}
