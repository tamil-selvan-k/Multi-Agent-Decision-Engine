import { DashboardService } from './dashboard.service';
import { asyncHandler } from '@utils/asyncHandler';
import { ApiResponse } from '@utils/ApiResponse';

export class DashboardController {
    public static getDashboard = asyncHandler(async () => {
        const data = await DashboardService.getDashboardData();
        return new ApiResponse(200, data, 'Dashboard metrics retrieved successfully');
    });
}
