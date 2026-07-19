import { Request } from 'express';
import { DecisionService } from './decision.service';
import { asyncHandler } from '@utils/asyncHandler';
import { ApiResponse } from '@utils/ApiResponse';

export class DecisionController {
    public static runDecision = asyncHandler(async (req: Request) => {
        const result = await DecisionService.runDecisionCycle(req.body);
        return new ApiResponse(202, result, 'Decision orchestration started');
    });

    public static getHistory = asyncHandler(async () => {
        const history = await DecisionService.getDecisionHistory();
        return new ApiResponse(200, history, 'Decision history retrieved successfully');
    });

    public static getDecisionById = asyncHandler(async (req: Request) => {
        const id = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
        const decision = await DecisionService.getDecisionById(id);
        return new ApiResponse(200, decision, 'Decision details retrieved successfully');
    });
}
