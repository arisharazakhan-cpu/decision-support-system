"""add data_source_id to metric_points

Revision ID: e921c3813f40
Revises: 1f2353761580
Create Date: 2026-02-19

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e921c3813f40"
down_revision = "1f2353761580"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1) Add nullable first so existing rows do not break
    op.add_column(
        "metric_points",
        sa.Column("data_source_id", sa.Integer(), nullable=True),
    )

    # 2) Index for faster lookups (SLA evaluation will filter by this)
    op.create_index(
        "ix_metric_points_data_source_id",
        "metric_points",
        ["data_source_id"],
    )

    # 3) Foreign key to data_sources.id
    op.create_foreign_key(
        "fk_metric_points_data_source_id_data_sources",
        "metric_points",
        "data_sources",
        ["data_source_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_metric_points_data_source_id_data_sources",
        "metric_points",
        type_="foreignkey",
    )
    op.drop_index("ix_metric_points_data_source_id", table_name="metric_points")
    op.drop_column("metric_points", "data_source_id")