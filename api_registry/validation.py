from database import UserPydantic, db


async def validate_credentials(
    credentials: UserPydantic,
) -> bool:
    user = await db.get_user_by_username(credentials.username)
    if user is None:
        return False
    return True