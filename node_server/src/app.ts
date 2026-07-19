import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { requestLogger } from '@middleware/logger';
import { errorHandler } from '@middleware/errorHandler';
import authRoutes from '@modules/auth/auth.routes';
import usersRoutes from '@modules/users/users.routes';
import dashboardRoutes from '@modules/dashboard/dashboard.routes';
import decisionRoutes from '@modules/decision/decision.routes';
import approvalRoutes from '@modules/approval/approval.routes';
import simulationRoutes from '@modules/simulation/simulation.routes';

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

// Mount Module Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/users', usersRoutes);
app.use('/api/v1/dashboard', dashboardRoutes);
app.use('/api/v1/decision', decisionRoutes);
app.use('/api/v1/approval', approvalRoutes);
app.use('/api/v1/simulation', simulationRoutes);

// Error Handling (Must be last)
app.use(errorHandler);

export default app;
