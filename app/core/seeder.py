from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.db.models.tenant import Tenant
from app.db.models.role import Role
from app.db.models.user import User
from app.db.models.user_role import UserRole
from app.core.security import hash_password

TENANT_SEEDS = [
    {
        "name": "Default",
        "domain": "default.example.com",
        "contact_email": "admin@example.com",
    }
]

ROLE_SEEDS = [
    {"name": "admin", "description": "Administrator with full access"},
    {"name": "manager", "description": "Manager with limited access"},
    {"name": "viewer", "description": "Read-only access"},
    {"name": "driver", "description": "Driver with tracking and trip access"},
]

USER_SEEDS = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "full_name": "Default Admin",
        "password": "SuperSecurePassword123",
        "tenant_name": "Default",
        "is_active": True,
        "is_verified": True,
        "roles": ["admin"]
    }
]

async def seed_tenants(session):
    for tenant_data in TENANT_SEEDS:
        result = await session.execute(select(Tenant).where(Tenant.name == tenant_data["name"]))
        tenant = result.scalar_one_or_none()
        if tenant is None:
            tenant = Tenant(**tenant_data)
            session.add(tenant)
            await session.commit()
            print(f"Seeded tenant '{tenant_data['name']}'.")
        else:
            print(f"Tenant '{tenant_data['name']}' already exists.")

async def seed_roles(session):
    for role_data in ROLE_SEEDS:
        result = await session.execute(select(Role).where(Role.name == role_data["name"]))
        role = result.scalar_one_or_none()
        if role is None:
            role = Role(**role_data)
            session.add(role)
            await session.commit()
            print(f"Seeded role '{role_data['name']}'.")
        else:
            print(f"Role '{role_data['name']}' already exists.")

async def seed_users(session):
    for user_data in USER_SEEDS:
        result = await session.execute(select(User).where(User.username == user_data["username"]))
        user = result.scalar_one_or_none()
        if user is None:
            tenant_result = await session.execute(select(Tenant).where(Tenant.name == user_data["tenant_name"]))
            tenant = tenant_result.scalar_one_or_none()

            if not tenant:
                print(f"Tenant '{user_data['tenant_name']}' not found for user '{user_data['username']}'. Skipping user seed.")
                continue

            hashed_pwd = hash_password(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=hashed_pwd,
                tenant_id=tenant.id,
                is_active=user_data.get("is_active", True),
                is_verified=user_data.get("is_verified", False),
            )
            session.add(user)
            await session.flush()  # to get user.id if needed
            # assign roles to user
            for role_name in user_data.get("roles", []):
                role_result = await session.execute(select(Role).where(Role.name == role_name))
                role = role_result.scalar_one_or_none()
                if role:
                    session.add(UserRole(user_id=user.id, role_id=role.id))
                else:
                    print(f"Role '{role_name}' not found for user '{user.username}'.")
            username = user.username  # store it before commit
            await session.commit()
            print(f"Seeded user '{username}'.")
        else:
            print(f"User '{user_data['username']}' already exists.")


async def run_seeders(session: AsyncSession):
    await seed_tenants(session)
    await seed_roles(session)
    await seed_users(session)
