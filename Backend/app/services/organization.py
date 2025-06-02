from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.organization import Organization
from app.models.authToken import AuthToken
from app.models.dataTypes import UserType
from app.core.security import get_password_hash, create_tokens, verify_password, create_access_token, create_refresh_token
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.schemas.auth import LoginRequest
from app.core.data import TokenInformation, RefreshTokenInformation

async def register_organization_user(
    db: AsyncSession,
    user_data: OrganizationCreate
) -> OrganizationResponse:
    """
    Registra un nuevo usuario de organización y devuelve sus datos y un token JWT.
    """
    # Verificar si el email ya existe
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    # Crear el usuario
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        type=UserType.organization
    )
    db.add(db_user)
    await db.flush()  # Para obtener el ID del usuario
    
    # Crear la organización
    db_organization = Organization(
        user_id=db_user.id,
        name=user_data.name,
        package_type=user_data.package_type
    )
    db.add(db_organization)
    await db.flush()  # Para obtener el ID de la organización
    
    # Crear los tokens
    access_token, refresh_token = create_tokens(
        TokenInformation(
            id=str(db_user.id),
            type=db_user.type
        )
    )
    
    # Crear el registro de tokens
    db_auth_token = AuthToken(
        user_id=db_user.id,
        token=access_token,
        refresh_token=refresh_token
    )
    db.add(db_auth_token)
    
    # Guardar todos los cambios
    await db.commit()
    
    # Refrescar los objetos para obtener los datos actualizados
    await db.refresh(db_user)
    await db.refresh(db_organization)
    await db.refresh(db_auth_token)
    
    return OrganizationResponse(
        id=db_user.id,
        email=db_user.email,
        type=db_user.type,
        name=db_organization.name,
        package_type=db_organization.package_type,
        created_at=db_user.created_at,
        access_token=access_token,
        refresh_token=refresh_token,
    )

async def login_organization_user(
    db: AsyncSession,
    user_data: LoginRequest
) -> OrganizationResponse:
    """
    Autentica a un usuario de organización y devuelve los tokens de acceso.
    """
    # Buscar usuario por email
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    # Verificar credenciales y tipo de usuario
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    if user.type != UserType.organization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint es solo para organizaciones"
        )
    
    # Buscar la organización
    query = select(Organization).where(Organization.user_id == user.id)
    result = await db.execute(query)
    organization = result.scalar_one_or_none()

    # Crear tokens con la información correcta
    token_info = TokenInformation(
        id=str(user.id),
        type=user.type
    )
    refresh_info = RefreshTokenInformation(
        id=str(user.id),
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
    
    return OrganizationResponse(
        id=user.id,
        email=user.email,
        type=user.type,
        name=organization.name,
        package_type=organization.package_type,
        created_at=user.created_at,
        access_token=access_token,
        refresh_token=refresh_token
    )

