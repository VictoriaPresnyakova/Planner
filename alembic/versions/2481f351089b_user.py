"""init

Revision ID: 2481f351089b
Revises: 
Create Date: 2024-06-01 15:20:37.985116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import ForeignKey


revision = '2481f351089b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    user = op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('surname', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('auth_token', sa.String(), nullable=True),
    )


def downgrade():
    pass
