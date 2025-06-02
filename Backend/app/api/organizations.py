from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.schemas.auth import LoginRequest
from app.services.organization import register_organization_user, login_organization_user

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("/register", response_model=OrganizationResponse)
async def create_new_organization(
    organization_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Crea una nueva organización.
    """
    try:
        return await register_organization_user(db, organization_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=OrganizationResponse)
async def organization_login(
    user_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Iniciar sesión como organización.
    """
    try:
        return await login_organization_user(db, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 