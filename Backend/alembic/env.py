import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.core.database import DATABASE_URL
from app.models import *  # Importamos todos los modelos

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    # Solo incluir tablas que no sean del sistema
    if type_ == "table":
        # Lista de tablas del sistema a ignorar
        system_tables = [
            "county",
            "state",
            "state_lookup",
            "topology",
            "secondary_unit_lookup",
            "featnames",
            "zip_state_loc",
            "tract",
            "geocode_settings",
            "zip_lookup_base",
            "tabblock20",
            "place_lookup",
            "addr",
            "loader_variables",
            "place",
            "zip_state",
            "spatial_ref_sys",
            "zip_lookup_all",
            "pagc_rules",
            "geocode_settings_default",
            "layer",
            "addrfeat",
            "loader_lookuptables",
            "faces",
            "countysub_lookup",
            "edges",
            "tabblock",
            "bg",
            "pagc_gaz",
            "county_lookup",
            "street_type_lookup",
            "loader_platform",
            "cousub",
            "zip_lookup",
            "pagc_lex",
            "direction_lookup",
            "zcta5",
        ]

        # Si es una tabla del sistema, no incluirla
        if name in system_tables:
            return False

        # Si es una tabla de nuestra aplicación, incluirla
        if name in target_metadata.tables:
            return True

        # Por defecto, no incluir otras tablas
        return False

    # Incluir otros objetos (índices, constraints, etc.)
    return True


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
