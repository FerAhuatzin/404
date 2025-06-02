from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Configuración de la base de datos desde variables de entorno
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "mydb")
DB_ECHO = os.getenv("DB_ECHO", "True").lower() == "true"

# Construir la URL de la base de datos
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el motor de la base de datos
engine = create_async_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    future=True
)

# Crear la sesión
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Crear la base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
async def get_db() -> AsyncSession:
    """
    Obtiene una sesión de base de datos.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
