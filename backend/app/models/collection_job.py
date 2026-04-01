"""
collection_jobs 테이블 모델.

정기 실행 작업(수집/분석 등) 정의를 관리한다.
job_name을 unique key로 사용하며, 스케줄 표현식(cron 등)을 저장할 수 있다.
"""

from sqlalchemy import BigInteger, Boolean, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class CollectionJob(Base, TimestampMixin):
    __tablename__ = "collection_jobs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    job_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    job_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 작업 유형
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    schedule_expr: Mapped[str | None] = mapped_column(String(100), nullable=True)  # 크론 또는 스케줄 표현식
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # relationships
    runs: Mapped[list["CollectionRun"]] = relationship(back_populates="job")

    __table_args__ = (
        Index("ix_collection_jobs_type_active", "job_type", "is_active"),
    )
