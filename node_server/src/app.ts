import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { requestLogger } from '@middleware/logger';
import { errorHandler } from '@middleware/errorHandler';
import authRoutes from '@modules/auth/auth.routes';
import { authenticateJWT, requireRole, requirePermission } from '@middleware/auth.middleware';

const app = express();

// Security Middlewares
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: '1mb' }));

// Request logging
app.use(requestLogger);

// Health Check
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Authentication Routes
app.use('/api/v1/auth', authRoutes);

// Protected Sample RBAC & Permission Endpoints
app.get('/api/v1/reports', authenticateJWT, requirePermission('view_reports'), (req, res) => {
    res.status(200).json({
        success: true,
        message: 'Access granted to reports',
        data: { reports: ['Q1 Financial Forecast', 'Inventory Valuation', 'Sales Conversion'] },
    });
});

app.post('/api/v1/orders/approve', authenticateJWT, requirePermission('approve_orders'), (req, res) => {
    res.status(200).json({
        success: true,
        message: 'Order approved successfully',
    });
});

app.post('/api/v1/inventory', authenticateJWT, requirePermission('manage_inventory'), (req, res) => {
    res.status(200).json({
        success: true,
        message: 'Inventory modified successfully',
    });
});

app.get('/api/v1/admin/dashboard', authenticateJWT, requireRole('Admin'), (req, res) => {
    res.status(200).json({
        success: true,
        message: 'Welcome Admin',
        data: { usersCount: 150, systemStatus: 'Optimal' },
    });
});

// Error Handling (Must be last)
app.use(errorHandler);

export default app;

