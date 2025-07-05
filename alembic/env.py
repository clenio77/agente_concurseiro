"""Alembic environment file (stub).
Autogenerates migrations from SQLAlchemy metadata.
"""
from __future__ import annotations

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings  # noqa: WPS433
from app.db.base import Base  # noqa: WPS433

# Alembic Config object
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URI)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)  # type: ignore[arg-type]

target_metadata = Base.metadata

def run_migrations_offline() -> None:  # noqa: D401
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:  # noqa: D401
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),  # type: ignore[arg-type]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()