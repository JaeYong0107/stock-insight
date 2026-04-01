"""
news_sentiment_runs 테이블 모델.

뉴스 기사별 감성 분석 실행 이력을 append-only로 저장한다.
동일 기사에 대해 여러 번 분석할 수 있으므로 강한 unique 제약은 두지 않는다.
"""

from sqlalchemy import BigInteger, ForeignKey, Index, String, Text, desc
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, CreatedAtMixin


class NewsSentimentRun(Base, CreatedAtMixin):
    __tablename__ = "news_sentiment_runs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    news_article_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("news_articles.id"), nullable=False)
    sentiment: Mapped[str] = mapped_column(String(20), nullable=False)  # positive, neutral, negative
    reason_summary: Mapped[str | None] = mapped_column(Text, nullable=True)  # 감성 근거 요약
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)  # 모델 공급자
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    raw_response: Mapped[str | None] = mapped_column(Text, nullable=True)  # 원문 응답 저장 옵션

    # relationship
    news_article: Mapped["NewsArticle"] = relationship(back_populates="sentiment_runs")

    __table_args__ = (
        Index("ix_news_sentiment_runs_article_created", "news_article_id", desc("created_at")),
        Index("ix_news_sentiment_runs_sentiment_created", "sentiment", desc("created_at")),
    )
