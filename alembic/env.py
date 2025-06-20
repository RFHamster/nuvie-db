import os
from logging.config import fileConfig

import dotenv

from sqlalchemy import engine_from_config, pool

from alembic import context

import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)


from nuvie_db.nuvie import SQLModelNuvie, metadata as nuvie_metadata


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name, disable_existing_loggers=False)


## IMPORTANT -> READ TO UNDERSTAND
# Import all personalized SQLModel Classes and metadatas
# This is the schema personalized classes (see core)

# from nuvie_db.another_schema import SQLModelSchema
# from nuvie_db.another_schema import metadata as another_schema_metadata

print(SQLModelNuvie.metadata)

schemas_metadata = {
    'nuvie': {
        'model': SQLModelNuvie,
        'metadata': SQLModelNuvie.metadata,
        'schema': nuvie_metadata.SCHEMA_NAME,
        'all_tables': nuvie_metadata.all_tables,
    },
    # 'another_schema': {
    #     'model': SQLModelSchema,
    #     'metadata': SQLModelSchema.metadata,
    #     'schema': another_schema_metadata.SCHEMA_NAME,
    #     'all_tables': another_schema_metadata.all_tables,
    # },
}


def get_metadata(schema: str):
    schema = schema.lower()
    if schema not in schemas_metadata:
        raise KeyError(
            f"Project '{schema}' not supported or not found in Alembic."
        )
    return schemas_metadata[schema]


SCHEMA = os.getenv('SCHEMA', 'nuvie')
schema_metadata = get_metadata(SCHEMA)

ENV_FILE = os.getenv('ENV_FILE', '.env')
loaded_env_vars = dotenv.load_dotenv(ENV_FILE, override=True)

print(f"Alembic | Loaded env vars from '{ENV_FILE}'? {loaded_env_vars}")
print(f'Alembic | POSTGRES_SERVER={os.getenv("POSTGRES_SERVER", "")}')
print(f'Alembic | POSTGRES_PORT={os.getenv("POSTGRES_PORT", "")}')


def get_url():
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', '')
    server = os.getenv('POSTGRES_SERVER', 'db')
    port = os.getenv('POSTGRES_PORT', '5432')
    db = os.getenv('POSTGRES_DB', 'app')
    return f'postgresql+psycopg://{user}:{password}@{server}:{port}/{db}'


def include_name(name, type_, parent_names):
    """Function used to filter out tables that are not managed by Alembic migrations for now"""
    if type_ == 'schema':
        # Alembic will only "watch" tables from the deafult schema or the one defined in nuvie_db.config.settings
        return name in [schema_metadata['schema']]
    elif type_ == 'table':
        # Alembic will only "watch" the tables which names are included here
        return name in [*schema_metadata['all_tables']]
    else:
        return True


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=schema_metadata['metadata'],
        include_name=include_name,
        include_schemas=True,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = context.config.attributes.get('connection', None)

    if connectable is None:
        configuration = context.config.get_section(
            context.config.config_ini_section
        )
        configuration['sqlalchemy.url'] = get_url()
        connectable = engine_from_config(
            configuration,
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=schema_metadata['metadata'],
            include_name=include_name,
            include_schemas=True,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
