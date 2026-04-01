"""
stock_price_daily 테이블 모델.

종목별 일봉 가격 데이터를 저장한다.
(stock_id, trade_date) 복합 unique 제약으로 중복을 방지하며,
DESC 인덱스를 통해 최신 데이터 조회를 최적화한다.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, ForeignKey, Index, Numeric, String, UniqueConstraint, desc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtMixin


class StockPriceDaily(Base, CreatedAtMixin):
    __tablename__ = "stock_price_daily"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("stocks.id"), nullable=False)
    trade_date: Mapped[date] = mapped_column(Date, nullable=False)
    open_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    high_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    low_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    close_price: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False)
    volume: Mapped[int] = mapped_column(BigInteger, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # 수집 소스 (예: KIS, KRX)
    collected_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    # relationship
    stock: Mapped["Stock"] = relationship(back_populates="prices")

    __table_args__ = (
        UniqueConstraint("stock_id", "trade_date", name="uq_stock_price_daily_stock_id_trade_date"),
        Index("ix_stock_price_daily_stock_trade_date_desc", "stock_id", desc("trade_date")),
        Index("ix_stock_price_daily_trade_date", "trade_date"),
        {"comment": "종목별 일봉 가격 데이터"},
    )
