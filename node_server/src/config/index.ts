import dotenv from 'dotenv';
import path from 'path';
import { z } from 'zod';

dotenv.config({ path: path.join(process.cwd(), '.env') });

const envSchema = z.object({
    PORT: z.string().default('3000').transform(Number),
    NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
    JWT_SECRET: z.string().min(32).default('secret-for-multi-agent-platform-dartx'),
    JWT_EXPIRES_IN: z.string().default('7d'),
    GOOGLE_CLIENT_ID: z.string().optional().default('sample_google_client_id.apps.googleusercontent.com'),
});

const envVars = envSchema.safeParse(process.env);

if (!envVars.success) {
    console.error('Invalid environment variables:', JSON.stringify(envVars.error.format(), null, 2));
    process.exit(1);
}

export const config = {
    port: envVars.data.PORT,
    nodeEnv: envVars.data.NODE_ENV,
    jwt: {
        secret: envVars.data.JWT_SECRET,
        expiresIn: envVars.data.JWT_EXPIRES_IN,
    },
    google: {
        clientId: envVars.data.GOOGLE_CLIENT_ID,
    },
};

