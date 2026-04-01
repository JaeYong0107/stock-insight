"""
stocks 테이블 모델.

국내 상장 주식 마스터 데이터를 관리한다.
symbol(종목코드)을 unique key로 사용하며, market/status 기반 복합 인덱스를 갖는다.
"""

from datetime import date

from sqlalchemy import BigInteger, Date, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Stock(Base, TimestampMixin):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    market: Mapped[str] = mapped_column(String(20), nullable=False)  # KOSPI, KOSDAQ
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="active")  # active, inactive, delisted
    listed_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    delisted_at: Mapped[date | None] = mapped_column(Date, nullable=True)

    # relationships
    prices: Mapped[list["StockPriceDaily"]] = relationship(back_populates="stock")
    news_links: Mapped[list["NewsArticleStock"]] = relationship(back_populates="stock")
    insights: Mapped[list["StockInsight"]] = relationship(back_populates="stock")
    collection_runs: Mapped[list["CollectionRun"]] = relationship(back_populates="stock")

    __table_args__ = (
        Index("ix_stocks_market_status", "market", "status"),
        Index("ix_stocks_name", "name"),
    )
