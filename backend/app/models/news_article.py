"""
news_articles 테이블 모델.

뉴스 기사 메타데이터 및 분석용 본문/요약을 저장한다.
url을 unique key로 사용하여 중복 수집을 방지한다.
"""

from datetime import datetime

from sqlalchemy import BigInteger, Index, String, Text, desc, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtMixin


class NewsArticle(Base, CreatedAtMixin):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(100), nullable=False)  # 언론사/출처
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, server_default="news")  # 콘텐츠 유형
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    body_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    url_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)  # 추후 URL 정규화 중복 방지 강화용
    published_at: Mapped[datetime] = mapped_column(nullable=False)
    collected_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    # relationships
    stock_links: Mapped[list["NewsArticleStock"]] = relationship(back_populates="news_article")
    sentiment_runs: Mapped[list["NewsSentimentRun"]] = relationship(back_populates="news_article")

    __table_args__ = (
        Index("ix_news_articles_published_at_desc", desc("published_at")),
        Index("ix_news_articles_source_name", "source_name"),
    )
