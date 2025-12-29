"""increase password_hash length to 255

Revision ID: 9b2c1b7d2c3f
Revises: 88a9595cce4d
Create Date: 2025-11-04 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b2c1b7d2c3f'
down_revision = '88a9595cce4d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'password_hash',
                    existing_type=sa.String(length=128),
                    type_=sa.String(length=255),
                    existing_nullable=True)


def downgrade():
    op.alter_column('users', 'password_hash',
                    existing_type=sa.String(length=255),
                    type_=sa.String(length=128),
                    existing_nullable=True)




