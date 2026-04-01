"""create all mvp tables

Revision ID: 001_mvp
Revises:
Create Date: 2026-04-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_mvp"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- stocks ---
    op.create_table(
        "stocks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("symbol", sa.String(16), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("market", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("listed_at", sa.Date(), nullable=True),
        sa.Column("delisted_at", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_stocks"),
        sa.UniqueConstraint("symbol", name="uq_stocks_symbol"),
    )
    op.create_index("ix_stocks_market_status", "stocks", ["market", "status"])
    op.create_index("ix_stocks_name", "stocks", ["name"])

    # --- stock_price_daily ---
    op.create_table(
        "stock_price_daily",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("stock_id", sa.BigInteger(), nullable=False),
        sa.Column("trade_date", sa.Date(), nullable=False),
        sa.Column("open_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("high_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("low_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("close_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("volume", sa.BigInteger(), nullable=False),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_stock_price_daily"),
        sa.ForeignKeyConstraint(
            ["stock_id"], ["stocks.id"],
            name="fk_stock_price_daily_stock_id_stocks",
        ),
        sa.UniqueConstraint("stock_id", "trade_date", name="uq_stock_price_daily_stock_id_trade_date"),
    )
    op.create_index(
        "ix_stock_price_daily_stock_trade_date_desc",
        "stock_price_daily",
        ["stock_id", sa.text("trade_date DESC")],
    )
    op.create_index("ix_stock_price_daily_trade_date", "stock_price_daily", ["trade_date"])

    # --- news_articles ---
    op.create_table(
        "news_articles",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("source_name", sa.String(100), nullable=False),
        sa.Column("source_type", sa.String(50), nullable=False, server_default="news"),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("body_text", sa.Text(), nullable=True),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("url_hash", sa.String(64), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_news_articles"),
        sa.UniqueConstraint("url", name="uq_news_articles_url"),
    )
    op.create_index(
        "ix_news_articles_published_at_desc",
        "news_articles",
        [sa.text("published_at DESC")],
    )
    op.create_index("ix_news_articles_source_name", "news_articles", ["source_name"])

    # --- news_article_stocks ---
    op.create_table(
        "news_article_stocks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("news_article_id", sa.BigInteger(), nullable=False),
        sa.Column("stock_id", sa.BigInteger(), nullable=False),
        sa.Column("mapping_method", sa.String(30), nullable=False, server_default="rule"),
        sa.Column("confidence_score", sa.Numeric(5, 4), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_news_article_stocks"),
        sa.ForeignKeyConstraint(
            ["news_article_id"], ["news_articles.id"],
            name="fk_news_article_stocks_news_article_id_news_articles",
        ),
        sa.ForeignKeyConstraint(
            ["stock_id"], ["stocks.id"],
            name="fk_news_article_stocks_stock_id_stocks",
        ),
        sa.UniqueConstraint(
            "news_article_id", "stock_id",
            name="uq_news_article_stocks_article_stock",
        ),
    )
    op.create_index(
        "ix_news_article_stocks_stock_article",
        "news_article_stocks",
        ["stock_id", "news_article_id"],
    )

    # --- news_sentiment_runs ---
    op.create_table(
        "news_sentiment_runs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("news_article_id", sa.BigInteger(), nullable=False),
        sa.Column("sentiment", sa.String(20), nullable=False),
        sa.Column("reason_summary", sa.Text(), nullable=True),
        sa.Column("provider", sa.String(50), nullable=True),
        sa.Column("model_name", sa.String(100), nullable=True),
        sa.Column("prompt_version", sa.String(50), nullable=True),
        sa.Column("raw_response", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_news_sentiment_runs"),
        sa.ForeignKeyConstraint(
            ["news_article_id"], ["news_articles.id"],
            name="fk_news_sentiment_runs_news_article_id_news_articles",
        ),
    )
    op.create_index(
        "ix_news_sentiment_runs_article_created",
        "news_sentiment_runs",
        ["news_article_id", sa.text("created_at DESC")],
    )
    op.create_index(
        "ix_news_sentiment_runs_sentiment_created",
        "news_sentiment_runs",
        ["sentiment", sa.text("created_at DESC")],
    )

    # --- stock_insights ---
    op.create_table(
        "stock_insights",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("stock_id", sa.BigInteger(), nullable=False),
        sa.Column("headline", sa.String(300), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("thesis", sa.Text(), nullable=True),
        sa.Column("evidence_summary", sa.Text(), nullable=True),
        sa.Column("input_price_from_date", sa.Date(), nullable=True),
        sa.Column("input_price_to_date", sa.Date(), nullable=True),
        sa.Column("input_news_from_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("input_news_to_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reference_close_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("provider", sa.String(50), nullable=True),
        sa.Column("model_name", sa.String(100), nullable=True),
        sa.Column("prompt_version", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_stock_insights"),
        sa.ForeignKeyConstraint(
            ["stock_id"], ["stocks.id"],
            name="fk_stock_insights_stock_id_stocks",
        ),
    )
    op.create_index(
        "ix_stock_insights_stock_created",
        "stock_insights",
        ["stock_id", sa.text("created_at DESC")],
    )
    op.create_index(
        "ix_stock_insights_created_desc",
        "stock_insights",
        [sa.text("created_at DESC")],
    )

    # --- stock_insight_evaluations ---
    op.create_table(
        "stock_insight_evaluations",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("stock_insight_id", sa.BigInteger(), nullable=False),
        sa.Column("evaluation_window_days", sa.Integer(), nullable=False),
        sa.Column("baseline_date", sa.Date(), nullable=False),
        sa.Column("baseline_close_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("evaluation_date", sa.Date(), nullable=False),
        sa.Column("evaluation_close_price", sa.Numeric(18, 4), nullable=False),
        sa.Column("price_change_rate", sa.Numeric(8, 4), nullable=False),
        sa.Column("direction_label", sa.String(20), nullable=False),
        sa.Column("is_direction_match", sa.Boolean(), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_stock_insight_evaluations"),
        sa.ForeignKeyConstraint(
            ["stock_insight_id"], ["stock_insights.id"],
            name="fk_stock_insight_evaluations_stock_insight_id_stock_insights",
        ),
        sa.UniqueConstraint(
            "stock_insight_id", "evaluation_window_days",
            name="uq_stock_insight_evaluations_insight_window",
        ),
    )
    op.create_index(
        "ix_stock_insight_evaluations_evaluated_desc",
        "stock_insight_evaluations",
        [sa.text("evaluated_at DESC")],
    )

    # --- collection_jobs ---
    op.create_table(
        "collection_jobs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("job_name", sa.String(100), nullable=False),
        sa.Column("job_type", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("schedule_expr", sa.String(100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_collection_jobs"),
        sa.UniqueConstraint("job_name", name="uq_collection_jobs_job_name"),
    )
    op.create_index("ix_collection_jobs_type_active", "collection_jobs", ["job_type", "is_active"])

    # --- collection_runs ---
    op.create_table(
        "collection_runs",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("collection_job_id", sa.BigInteger(), nullable=False),
        sa.Column("stock_id", sa.BigInteger(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("processed_count", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_collection_runs"),
        sa.ForeignKeyConstraint(
            ["collection_job_id"], ["collection_jobs.id"],
            name="fk_collection_runs_collection_job_id_collection_jobs",
        ),
        sa.ForeignKeyConstraint(
            ["stock_id"], ["stocks.id"],
            name="fk_collection_runs_stock_id_stocks",
        ),
    )
    op.create_index(
        "ix_collection_runs_job_started",
        "collection_runs",
        ["collection_job_id", sa.text("started_at DESC")],
    )
    op.create_index(
        "ix_collection_runs_status_started",
        "collection_runs",
        ["status", sa.text("started_at DESC")],
    )
    op.create_index(
        "ix_collection_runs_stock_started",
        "collection_runs",
        ["stock_id", sa.text("started_at DESC")],
    )


def downgrade() -> None:
    op.drop_table("collection_runs")
    op.drop_table("collection_jobs")
    op.drop_table("stock_insight_evaluations")
    op.drop_table("stock_insights")
    op.drop_table("news_sentiment_runs")
    op.drop_table("news_article_stocks")
    op.drop_table("news_articles")
    op.drop_table("stock_price_daily")
    op.drop_table("stocks")
