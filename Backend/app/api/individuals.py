from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.services.individual import register_individual_user, login_individual_user
from app.schemas.individual import IndividualUserCreate, IndividualUserResponse
from app.schemas.auth import LoginRequest


router = APIRouter(
    prefix="/individuals",
    tags=["individuals"]
)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

@router.post("/register", response_model=IndividualUserResponse)
async def register_user(
    user_data: IndividualUserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registra un nuevo usuario individual.
    """
    try:
        return await register_individual_user(db, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=IndividualUserResponse)
async def individual_login(
    user_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    "Iniciar sesion en app mobil"
    try:
        return await login_individual_user(db, user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

"""
@router.get("/login/google")
async def google_login(request: Request):
    #Inicia el proceso de autenticación con Google.
    
    redirect_uri = "http://localhost:8000/individuals/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri, prompt="consent")

@router.get("/auth/google/callback")
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):

    #Callback para la autenticación con Google.

    try:
        token = await oauth.auth_demo.authorize_access_token(request)
        user_info_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f'Bearer {token["access_token"]}'}
        google_response = await request.get(user_info_endpoint, headers=headers)
        user_info = google_response.json()


        user = token.get("userinfo")
        expires_in = token.get("expires_in")
        user_id = user.get("sub")
        iss = user.get("iss")
        email = user.get("email")
        first_logged_in = datetime.utcnow()
        last_accessed = datetime.utcnow()

        name = user_info.get("name")
        picture = user_info.get("picture")

        if iss not in ["https://accounts.google.com", "accounts.google.com"]:
            raise HTTPException(status_code=401, detail="Google authentication failed.")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Google authentication failed.")

        google_user = GoogleUserInfo(
            email=email,
            name=name,
            picture=picture
        )
            
        return await login_with_google(db, google_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en la autenticación con Google: {str(e)}"
        ) 
"""
