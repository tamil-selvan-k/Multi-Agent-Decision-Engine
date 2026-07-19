import { Request } from 'express';
import { z } from 'zod';
import { SimulationService } from './simulation.service';
import { asyncHandler } from '@utils/asyncHandler';
import { ApiResponse } from '@utils/ApiResponse';
import { AppError } from '@utils/AppError';

const simulationSchema = z.object({
    demandIncrease: z.number().min(0),
    budgetReduction: z.number().min(0),
});

export class SimulationController {
    public static runSimulation = asyncHandler(async (req: Request) => {
        const parseResult = simulationSchema.safeParse(req.body);
        if (!parseResult.success) {
            throw new AppError('Invalid simulation payload. Numeric demandIncrease and budgetReduction required', 400, parseResult.error.issues);
        }
        const results = await SimulationService.runSimulation(parseResult.data);
        return new ApiResponse(200, results, 'Simulation scenario executed successfully');
    });
}
