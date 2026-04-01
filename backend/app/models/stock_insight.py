"""
stock_insights 테이블 모델.

종목 기준 AI 인사이트 스냅샷을 append-only로 저장한다.
생성 시점의 가격/뉴스 입력 범위 메타데이터를 함께 기록하여
추후 사후 평가(stock_insight_evaluations)와 연결한다.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, ForeignKey, Index, Numeric, String, Text, desc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtMixin


class StockInsight(Base, CreatedAtMixin):
    __tablename__ = "stock_insights"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("stocks.id"), nullable=False)
    headline: Mapped[str | None] = mapped_column(String(300), nullable=True)  # 한 줄 요약 제목
    summary: Mapped[str] = mapped_column(Text, nullable=False)  # 종합 인사이트 본문
    thesis: Mapped[str | None] = mapped_column(Text, nullable=True)  # 핵심 주장
    evidence_summary: Mapped[str | None] = mapped_column(Text, nullable=True)  # 근거 요약
    input_price_from_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    input_price_to_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    input_news_from_at: Mapped[datetime | None] = mapped_column(nullable=True)
    input_news_to_at: Mapped[datetime | None] = mapped_column(nullable=True)
    reference_close_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)  # 생성 시점 기준 종가
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # relationships
    stock: Mapped["Stock"] = relationship(back_populates="insights")
    evaluations: Mapped[list["StockInsightEvaluation"]] = relationship(back_populates="insight")

    __table_args__ = (
        Index("ix_stock_insights_stock_created", "stock_id", desc("created_at")),
        Index("ix_stock_insights_created_desc", desc("created_at")),
    )
