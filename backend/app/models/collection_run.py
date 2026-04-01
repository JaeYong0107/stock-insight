"""
collection_runs 테이블 모델.

작업 실행 이력을 기록한다.
각 실행은 하나의 collection_job에 속하며, 선택적으로 특정 종목(stock_id)과 연결된다.
status(pending/running/success/failed)로 실행 상태를 추적한다.
"""

from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Index, Integer, String, Text, desc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtMixin


class CollectionRun(Base, CreatedAtMixin):
    __tablename__ = "collection_runs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    collection_job_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("collection_jobs.id"), nullable=False)
    stock_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("stocks.id"), nullable=True)  # 종목 단위 작업 추적용
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # pending, running, success, failed
    started_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)
    processed_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # relationships
    job: Mapped["CollectionJob"] = relationship(back_populates="runs")
    stock: Mapped["Stock | None"] = relationship(back_populates="collection_runs")

    __table_args__ = (
        Index("ix_collection_runs_job_started", "collection_job_id", desc("started_at")),
        Index("ix_collection_runs_status_started", "status", desc("started_at")),
        Index("ix_collection_runs_stock_started", "stock_id", desc("started_at")),
    )
