"""task

Revision ID: 9c57557701ce
Revises: 2481f351089b
Create Date: 2024-11-24 14:00:14.541072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey

revision = '9c57557701ce'
down_revision = '2481f351089b'
branch_labels = None
depends_on = None


def upgrade():
    from repositories.db.enums import TaskStatus
    op.execute("DROP TYPE IF EXISTS taskstatus;")
    task = op.create_table(
        'task',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Enum(TaskStatus, values_callable=lambda obj: [e.value for e in obj]),
                  nullable=False, server_default=TaskStatus.NEW),
        sa.Column('assigned_user_id', sa.Integer, ForeignKey("user.id", ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('deadline', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer, ForeignKey("user.id", ondelete='SET NULL'), nullable=False),
    )


def downgrade():
    pass
