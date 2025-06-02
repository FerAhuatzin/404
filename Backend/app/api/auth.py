from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RefreshTokenRequest
from app.services.auth import login, refresh_tokens,logout
from app.core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login_user(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Inicia sesión de un usuario.
    """
    try:
        return await login(db, login_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.post("/refresh")
async def refresh_token(
    refresh_token: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresca el token de acceso usando el token de refresh.
    """
    try:
        return await refresh_tokens(db, refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) 

@router.post("/logout")
async def logout_user(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    """
    Cierra la sesión del usuario actual.
    """
    try:
        await logout(db, user_id)
        return {"message": "Sesión cerrada correctamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cerrar la sesión: {str(e)}"
        ) 