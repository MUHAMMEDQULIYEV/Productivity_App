"""Initial database schema migration.

Revision ID: 001
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── Enums ─────────────────────────────────────────────────────────────────
    task_category = postgresql.ENUM(
        "work", "study", "learning", "personal", name="task_category"
    )
    task_priority = postgresql.ENUM(
        "high", "medium", "low", name="task_priority"
    )
    task_status = postgresql.ENUM(
        "not_started", "in_progress", "completed", "archived",
        name="task_status"
    )
    deck_language = postgresql.ENUM(
        "english", "korean", name="deck_language"
    )
    deck_source_type = postgresql.ENUM(
        "youtube", "manual", "upload", name="deck_source_type"
    )

    # ── tasks ─────────────────────────────────────────────────────────────────
    op.create_table(
        "tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("category", task_category, nullable=False, server_default="personal"),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("priority", task_priority, nullable=False, server_default="medium"),
        sa.Column("status", task_status, nullable=False, server_default="not_started"),
        sa.Column("estimated_duration", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ── notes ─────────────────────────────────────────────────────────────────
    op.create_table(
        "notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", sa.Text, nullable=False, server_default=""),
        sa.Column("tags", postgresql.JSON, nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ── flashcard_decks ───────────────────────────────────────────────────────
    op.create_table(
        "flashcard_decks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("language", deck_language, nullable=False, server_default="english"),
        sa.Column("source_type", deck_source_type, nullable=False, server_default="manual"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ── flashcards ────────────────────────────────────────────────────────────
    op.create_table(
        "flashcards",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "deck_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("flashcard_decks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("front", sa.Text, nullable=False),
        sa.Column("back", sa.Text, nullable=False),
        sa.Column("ease_factor", sa.Float, nullable=False, server_default="2.5"),
        sa.Column("interval", sa.Integer, nullable=False, server_default="1"),
        sa.Column("repetitions", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_reviewed", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_review", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ── language_vocabulary ───────────────────────────────────────────────────
    op.create_table(
        "language_vocabulary",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("word", sa.String(255), nullable=False),
        sa.Column("language", sa.String(50), nullable=False, server_default="english"),
        sa.Column("translation", sa.String(512), nullable=True),
        sa.Column("frequency_count", sa.Integer, nullable=False, server_default="1"),
        sa.Column("source_url", sa.String(1024), nullable=True),
        sa.Column("learned", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("date_learned", sa.Date, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ── productivity_analytics ────────────────────────────────────────────────
    op.create_table(
        "productivity_analytics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("tasks_completed", sa.Integer, nullable=False, server_default="0"),
        sa.Column("tasks_total", sa.Integer, nullable=False, server_default="0"),
        sa.Column("category_breakdown", postgresql.JSON, nullable=False, server_default="{}"),
        sa.Column("completion_rate", sa.Float, nullable=False, server_default="0"),
    )

    # ── language_progress ─────────────────────────────────────────────────────
    op.create_table(
        "language_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("language", sa.String(50), nullable=False, server_default="english"),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("words_learned", sa.Integer, nullable=False, server_default="0"),
        sa.Column("flashcard_accuracy", sa.Float, nullable=False, server_default="0"),
        sa.Column("time_spent", sa.Integer, nullable=False, server_default="0"),
        sa.Column("topics_studied", postgresql.JSON, nullable=False, server_default="[]"),
    )


def downgrade() -> None:
    op.drop_table("language_progress")
    op.drop_table("productivity_analytics")
    op.drop_table("language_vocabulary")
    op.drop_table("flashcards")
    op.drop_table("flashcard_decks")
    op.drop_table("notes")
    op.drop_table("tasks")

    from sqlalchemy.dialects import postgresql
    from alembic import op as _op

    for name in ("task_category", "task_priority", "task_status", "deck_language", "deck_source_type"):
        postgresql.ENUM(name=name).drop(_op.get_bind(), checkfirst=True)
