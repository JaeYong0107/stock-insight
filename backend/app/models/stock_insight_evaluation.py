"""
stock_insight_evaluations 테이블 모델.

인사이트 사후 평가 결과를 저장한다.
하나의 인사이트에 대해 평가 윈도우(7/30/90/180일)별로 한 건씩 생성된다.
(stock_insight_id, evaluation_window_days) 복합 unique 제약으로 중복을 방지한다.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint, desc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtMixin


class StockInsightEvaluation(Base, CreatedAtMixin):
    __tablename__ = "stock_insight_evaluations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    stock_insight_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("stock_insights.id"), nullable=False)
    evaluation_window_days: Mapped[int] = mapped_column(Integer, nullable=False)  # 7, 30, 90, 180
    baseline_date: Mapped[date] = mapped_column(Date, nullable=False)  # 기준 가격 일자
    baseline_close_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    evaluation_date: Mapped[date] = mapped_column(Date, nullable=False)  # 평가 가격 일자
    evaluation_close_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    price_change_rate: Mapped[Decimal] = mapped_column(Numeric(8, 4), nullable=False)  # 수익률/변화율
    direction_label: Mapped[str] = mapped_column(String(20), nullable=False)  # up, down, flat
    is_direction_match: Mapped[bool | None] = mapped_column(Boolean, nullable=True)  # 방향성 적중 여부 (nullable: 인사이트에 방향성이 없을 수 있음)
    evaluated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    # relationship
    insight: Mapped["StockInsight"] = relationship(back_populates="evaluations")

    __table_args__ = (
        UniqueConstraint(
            "stock_insight_id", "evaluation_window_days",
            name="uq_stock_insight_evaluations_insight_window",
        ),
        Index("ix_stock_insight_evaluations_evaluated_desc", desc("evaluated_at")),
    )
