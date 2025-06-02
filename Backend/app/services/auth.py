from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import create_access_token, create_refresh_token, verify_password, get_password_hash, verify_token, refresh_tokens_action
from app.models.user import User
from app.models.authToken import AuthToken
from app.schemas.auth import LoginRequest, RefreshTokenRequest, RefreshTokenResponse, UserInfoResponse
from app.core.data import TokenInformation, RefreshTokenInformation
from jose import JWTError, jwt

async def login(db: AsyncSession, login_data: LoginRequest) -> dict:
    """
    Autentica a un usuario y devuelve los tokens de acceso.
    """
    query = select(User).where(User.email == login_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Crear tokens con la información correcta
    token_info = TokenInformation(
        id=user.id,
        type=user.type
    )
    refresh_info = RefreshTokenInformation(
        id=user.id,
        type=user.type
    )
    
    access_token = create_access_token(token_info.model_dump())
    refresh_token = create_refresh_token(refresh_info.model_dump())
    
    # Guardar tokens en la base de datos
    auth_token = AuthToken(
        user_id=user.id,
        token=access_token,
        refresh_token=refresh_token
    )
    db.add(auth_token)
    await db.commit()
    
    return UserInfoResponse(
        id=user.id,
        email=user.email,
        type=user.type,
        access_token=access_token,
        refresh_token=refresh_token
    )

async def refresh_tokens(db: AsyncSession, refresh_data: RefreshTokenRequest) -> RefreshTokenResponse:
    """
    Refresca los tokens de acceso y actualiza la base de datos.
    """
    try:
        access_token, refresh_token, user_id = refresh_tokens_action(refresh_data.refresh_token)
        # Actualizar tokens en la base de datos
        query = select(AuthToken).where(AuthToken.user_id == user_id)
        result = await db.execute(query)
        auth_token = result.scalar_one_or_none()

        if auth_token:
            auth_token.token = access_token
            auth_token.refresh_token = refresh_token
        else:
            auth_token = AuthToken(
                user_id=user_id,
                token=access_token,
                refresh_token=refresh_token
            )
            db.add(auth_token)

        await db.commit()

        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

async def logout(db: AsyncSession, user_id: int) -> None:
    """
    Cierra la sesión de un usuario eliminando sus tokens.
    """
    query = select(AuthToken).where(AuthToken.user_id == user_id)
    result = await db.execute(query)
    auth_token = result.scalar_one_or_none()
    
    if auth_token:
        await db.delete(auth_token)
        await db.commit() 