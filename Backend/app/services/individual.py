from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.individual import Individual
from app.models.authToken import AuthToken
from app.models.dataTypes import UserType
from app.core.security import get_password_hash, create_tokens, verify_password, create_access_token, create_refresh_token
from app.schemas.individual import IndividualUserCreate, IndividualUserResponse
from app.schemas.auth import LoginRequest
from app.core.data import TokenInformation, RefreshTokenInformation

async def register_individual_user(
    db: AsyncSession,
    user_data: IndividualUserCreate
) -> IndividualUserResponse:
    """
    Registra un nuevo usuario individual y devuelve sus datos y un token JWT.
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
        type=UserType.individual
    )
    db.add(db_user)
    await db.flush()  # Para obtener el ID del usuario
    
    # Crear el perfil individual
    db_individual = Individual(
        user_id=db_user.id,
        full_name=user_data.full_name
    )
    db.add(db_individual)
    await db.flush()  # Para obtener el ID del individual
    
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
    await db.refresh(db_individual)
    await db.refresh(db_auth_token)
    
    return IndividualUserResponse(
        id=db_user.id,
        email=db_user.email,
        type=db_user.type,
        full_name=db_individual.full_name,
        created_at=db_user.created_at,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def login_individual_user( 
    db: AsyncSession,
    user_data: LoginRequest
) -> IndividualUserResponse:
    """
    Autentica a un usuario individual y devuelve los tokens de acceso.
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
    
    if user.type != UserType.individual:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este endpoint es solo para usuarios individuales"
        )
    
    # Buscar usuario por email
    query = select(Individual).where(User.email == user_data.email)
    result = await db.execute(query)
    individual = result.scalar_one_or_none()

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
    
    return IndividualUserResponse(
        id=user.id,
        email=user.email,
        type=user.type,
        full_name=individual.full_name,
        created_at=user.created_at,
        access_token=access_token,
        refresh_token=refresh_token
    )


"""
async def login_with_google(
    db: AsyncSession,
    google_user: GoogleUserInfo
) -> IndividualUserResponse:

    #Autentica o registra un usuario usando Google OAuth.

    try:
        # Buscar si el usuario ya existe
        query = select(User, Individual).join(
            Individual,
            User.id == Individual.user_id
        ).where(User.email == google_user.email)
        
        result = await db.execute(query)
        user_data = result.first()
        
        if user_data:
            # Usuario existente - actualizar tokens
            db_user, db_individual = user_data
        else:
            # Crear nuevo usuario
            db_user = User(
                email=google_user.email,
                type=UserType.individual
            )
            db.add(db_user)
            await db.flush()
            
            # Crear perfil individual
            db_individual = Individual(
                user_id=db_user.id,
                full_name=google_user.name
            )
            db.add(db_individual)
            await db.flush()
        
        # Crear tokens de acceso
        access_token, refresh_token = create_tokens(
            TokenInformation(
                id=str(db_user.id),
                type=db_user.type
            )
        )
        
        # Actualizar o crear el registro de tokens
        query = select(AuthToken).where(AuthToken.user_id == db_user.id)
        result = await db.execute(query)
        db_auth_token = result.scalar_one_or_none()
        
        if db_auth_token:
            db_auth_token.token = access_token
            db_auth_token.refresh_token = refresh_token
        else:
            db_auth_token = AuthToken(
                user_id=db_user.id,
                token=access_token,
                refresh_token=refresh_token
            )
            db.add(db_auth_token)
        
        await db.commit()
        await db.refresh(db_auth_token)
        
        return IndividualUserResponse(
            id=db_user.id,
            email=db_user.email,
            type=db_user.type,
            full_name=db_individual.full_name,
            created_at=db_user.created_at,
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la autenticación con Google: {str(e)}"
        ) 
    
"""
