import typing as t

from nuvie_db.core.constants import convention
from nuvie_db.nuvie.metadata import SCHEMA_NAME
from datetime import datetime
from sqlmodel import TIMESTAMP, Field, text, MetaData, SQLModel


class SQLModelNuvie(SQLModel):
    metadata = MetaData(schema=SCHEMA_NAME, naming_convention=convention)


class BaseModelNuvie_(SQLModelNuvie):
    created_at: t.Optional[datetime] = Field(
        default_factory=datetime.utcnow, nullable=True
    )

    # https://github.com/fastapi/sqlmodel/discussions/743
    updated_at: t.Optional[datetime] = Field(
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={
            'server_default': text('CURRENT_TIMESTAMP'),
            'server_onupdate': text('CURRENT_TIMESTAMP'),
        },
        nullable=True,
        default_factory=datetime.utcnow,
    )
    deleted_at: t.Optional[datetime] = Field(nullable=True, default=None)
