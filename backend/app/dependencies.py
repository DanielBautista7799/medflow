import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.user import User
from app.security import decode_access_token
from app.database import AsyncSessionLocal


from collections.abc import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

#returns token from token storage basically a get token function
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# figure out who you are using the token you already got
async def get_current_user(
        #calls get token on waht ever is passed
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exeption = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        #just bascially a comment for readability
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload=decode_access_token(token)
        username= payload.get("sub")

        if username is None:
            raise credentials_exeption
    except jwt.InvalidTokenError:
        raise credentials_exeption
    
    result = await db.execute(
        select(User).where(User.username == username)
    )

    user =  result.scalar_one_or_none()
    if user is None:
        raise credentials_exeption
    
    return user

#* means it can multiple or one
#require role configures the rules to which users are allowed to perform actions
def require_role(*allowed_roles: UserRole):
    #role checker checks current role must be nested to check against allowed roles
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role.value}' is not permitted to perform this action"
            )
        return current_user
    return role_checker #returns function with parameters of allowed roles

