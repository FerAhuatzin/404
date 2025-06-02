from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, individuals, organizations

app = FastAPI(
    title="404 Carbon Reduction API",
    version=1.0,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(individuals.router)
app.include_router(organizations.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API"}
