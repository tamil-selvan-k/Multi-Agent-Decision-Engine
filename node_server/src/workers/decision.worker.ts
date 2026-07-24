import { parentPort, workerData } from 'worker_threads';

async function executeDecisionTask() {
    if (!parentPort) {
        throw new Error('This script must be run as a worker thread.');
    }

    const { sessionId, parameters, pythonServiceUrl } = workerData;

    try {
        const response = await fetch(pythonServiceUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                parameters: parameters || {},
            }),
        });

        const data: any = await response.json();

        if (!response.ok) {
            parentPort.postMessage({
                success: false,
                status: response.status,
                message: data.message || 'Error occurred in Python AI service',
                errors: data.errors || [],
            });
            return;
        }

        parentPort.postMessage({
            success: true,
            data,
        });
    } catch (err: any) {
        parentPort.postMessage({
            success: false,
            status: 500,
            message: err.message || 'Worker thread failed to communicate with Python service',
            errors: [],
        });
    }
}

executeDecisionTask();
