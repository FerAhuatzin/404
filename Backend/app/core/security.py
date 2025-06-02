from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from typing import Optional, Tuple
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.data import TokenInformation, RefreshTokenInformation
import os
from app.models.user import User

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_aqui")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

def get_password_hash(password: str) -> str:
    """
    Genera un hash de la contraseña.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash.
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash de la contraseña almacenado
        
    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT.
    
    Args:
        data: Información del token
        expires_delta: Tiempo de expiración del token
        
    Returns:
        str: Token JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """
    Crea un token de actualización JWT.
    
    Args:
        data: Información del refresh token
        
    Returns:
        str: Refresh token JWT
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_tokens(data: TokenInformation) -> Tuple[str, str]:
    """
    Crea un par de tokens (access y refresh).
    
    Args:
        data: Información del token
        
    Returns:
        Tuple[str, str]: Tupla con (access_token, refresh_token)
    """
    access_token = create_access_token(data.model_dump())
    refresh_token = create_refresh_token(data.model_dump())
    return access_token, refresh_token

def verify_token(token: str) -> dict:
    """
    Verifica y decodifica un token JWT.
    
    Args:
        token: Token JWT a verificar
        
    Returns:
        dict: Datos decodificados del token
        
    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        ) 

def refresh_tokens_action(refresh_token: str) -> Tuple[str, str, int]:
    """
    Refresca Tokens en caso que el de acceso este vencido 
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        #si el refresh_token es valido todavia, manda a llamar a create_tokens
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: no es un refresh token"
            )
            
        # Crear nuevos tokens usando la información del payload
        token_info = TokenInformation(
            id=payload.get("id"),
            type=payload.get("type")
        )
        refresh_info = RefreshTokenInformation(
            id=payload.get("id"),
            type=payload.get("type")
        )

        access_token = create_access_token(token_info.model_dump())
        refresh_token_created = create_refresh_token(refresh_info.model_dump())
        
        # Devolver los tokens junto con el ID del usuario
        return access_token, refresh_token_created, int(payload.get("id"))
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """
    Obtiene el ID del usuario actual desde el token JWT.
    """
    try:
        payload = verify_token(credentials.credentials)
        return int(payload.get("id"))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        ) 
