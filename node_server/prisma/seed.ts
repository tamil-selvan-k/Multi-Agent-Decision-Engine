import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
    console.log('Seeding roles and permissions...');

    // Standard Permissions
    const permissionsData = [
        { name: 'view_reports', description: 'Can view analytics and operational reports' },
        { name: 'approve_orders', description: 'Can approve or reject pending orders' },
        { name: 'manage_inventory', description: 'Can create, update, or remove inventory stock' },
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
            name: 'Admin',
            description: 'Full access to all system resources and administrative features',
            permissions: ['view_reports', 'approve_orders', 'manage_inventory'],
        },
        {
            name: 'Manager',
            description: 'Can manage operations, approve orders, and view reports',
            permissions: ['view_reports', 'approve_orders'],
        },
        {
            name: 'Employee',
            description: 'Standard access to view reports and basic features',
            permissions: ['view_reports'],
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

        // Link permissions
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
