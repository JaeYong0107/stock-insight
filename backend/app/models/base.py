"""
SQLAlchemy 모델 공통 베이스 및 mixin 정의.

- Base: 모든 모델의 부모 클래스. naming convention을 포함한 MetaData를 공유한다.
- TimestampMixin: created_at + updated_at 이 모두 필요한 테이블용.
- CreatedAtMixin: created_at만 필요한 append-only 테이블용.
"""

from datetime import datetime

from sqlalchemy import MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Alembic autogenerate가 일관된 이름을 생성하도록 하는 naming convention
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)


class TimestampMixin:
    """created_at / updated_at 공통 mixin. stocks, collection_jobs 등에서 사용."""

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CreatedAtMixin:
    """created_at만 필요한 테이블용 mixin. append-only 성격의 테이블에서 사용."""

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
