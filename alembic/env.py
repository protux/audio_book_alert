from logging.config import fileConfig

from alembic import context
from alembic.script import ScriptDirectory
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from audio_book_alert.database import utils
from audio_book_alert.database.orm import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', utils.get_connection_string())

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        db_schema = utils.get_database_schema()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=db_schema or None,
            include_schemas=True if db_schema else False,
            compare_type=True,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            db_url = utils.get_connection_string()
            if not db_url.startswith('sqlite'):
                if db_schema:
                    context.execute(f'CREATE SCHEMA IF NOT EXISTS "{db_schema}"')
                    context.execute(f'SET search_path TO "{db_schema}"')
            context.run_migrations()


def process_revision_directives(context, revision, directives):
    migration_script = directives[0]
    head_revision = ScriptDirectory.from_config(context.config).get_current_head()

    if head_revision is None:
        new_rev_id = 1
    else:
        last_rev_id = int(head_revision.lstrip('0'))
        new_rev_id = last_rev_id + 1

    migration_script.rev_id = '{0:04}'.format(new_rev_id)


if not context.is_offline_mode():
    run_migrations_online()
