"""
news_article_stocks 테이블 모델.

뉴스 기사와 종목 간의 N:M 연결 테이블.
(news_article_id, stock_id) 복합 unique 제약으로 동일 매핑 중복을 방지한다.
"""

from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Index, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtMixin


class NewsArticleStock(Base, CreatedAtMixin):
    __tablename__ = "news_article_stocks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    news_article_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("news_articles.id"), nullable=False)
    stock_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("stocks.id"), nullable=False)
    mapping_method: Mapped[str] = mapped_column(String(30), nullable=False, server_default="rule")  # rule, search, manual, ai
    confidence_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)  # AI/스코어 기반 연결 시 활용

    # relationships
    news_article: Mapped["NewsArticle"] = relationship(back_populates="stock_links")
    stock: Mapped["Stock"] = relationship(back_populates="news_links")

    __table_args__ = (
        UniqueConstraint("news_article_id", "stock_id", name="uq_news_article_stocks_article_stock"),
        Index("ix_news_article_stocks_stock_article", "stock_id", "news_article_id"),
    )
