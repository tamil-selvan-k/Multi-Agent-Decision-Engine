import { PrismaClient } from '@prisma/client';
import { RoleEnum, PermissionEnum } from '../src/types/rbac.enum';

const prisma = new PrismaClient();

async function main() {
    console.log('Seeding roles and permissions using RBAC enums...');

    // Standard Permissions defined by enterprise specifications
    const permissionsData = [
        { name: PermissionEnum.RUN_DECISION, description: 'Can trigger autonomous multi-agent decision cycles' },
        { name: PermissionEnum.APPROVE_DECISION, description: 'Can approve or reject operational agent decisions' },
        { name: PermissionEnum.VIEW_DASHBOARD, description: 'Can view platform operational dashboard and KPIs' },
        { name: PermissionEnum.MANAGE_USERS, description: 'Can manage platform user accounts and role assignments' },
        { name: PermissionEnum.RUN_SIMULATION, description: 'Can run what-if operational market simulations' },
    ];

    const permissionsMap = new Map<string, string>();
    for (const perm of permissionsData) {
        const p = await prisma.permission.upsert({
            where: { name: perm.name },
            update: { description: perm.description },
            create: perm,
        });
        permissionsMap.set(perm.name, p.id);
    }

    // Standard Roles & Permission Mappings
    const rolesData = [
        {
            name: RoleEnum.ADMIN,
            description: 'Full administrative access to users, agent orchestrations, approvals, and simulations',
            permissions: [
                PermissionEnum.RUN_DECISION,
                PermissionEnum.APPROVE_DECISION,
                PermissionEnum.VIEW_DASHBOARD,
                PermissionEnum.MANAGE_USERS,
                PermissionEnum.RUN_SIMULATION,
            ],
        },
        {
            name: RoleEnum.MANAGER,
            description: 'Operational manager with decision execution, approval, dashboard, and simulation rights',
            permissions: [
                PermissionEnum.RUN_DECISION,
                PermissionEnum.APPROVE_DECISION,
                PermissionEnum.VIEW_DASHBOARD,
                PermissionEnum.RUN_SIMULATION,
            ],
        },
        {
            name: RoleEnum.ANALYST,
            description: 'Business analyst capable of viewing dashboards, running decisions, and market simulations',
            permissions: [
                PermissionEnum.RUN_DECISION,
                PermissionEnum.VIEW_DASHBOARD,
                PermissionEnum.RUN_SIMULATION,
            ],
        },
        {
            name: RoleEnum.EXECUTIVE,
            description: 'Executive user with high-level dashboard oversight and final decision approval authority',
            permissions: [
                PermissionEnum.VIEW_DASHBOARD,
                PermissionEnum.APPROVE_DECISION,
            ],
        },
    ];

    for (const roleData of rolesData) {
        const role = await prisma.role.upsert({
            where: { name: roleData.name },
            update: { description: roleData.description },
            create: {
                name: roleData.name,
                description: roleData.description,
            },
        });

        for (const permName of roleData.permissions) {
            const permId = permissionsMap.get(permName);
            if (permId) {
                await prisma.rolePermission.upsert({
                    where: {
                        roleId_permissionId: {
                            roleId: role.id,
                            permissionId: permId,
                        },
                    },
                    update: {},
                    create: {
                        roleId: role.id,
                        permissionId: permId,
                    },
                });
            }
        }
    }

    console.log('Seeding completed successfully!');
}

main()
    .catch((e) => {
        console.error('Error during seeding:', e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
