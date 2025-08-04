"""Fusionando múltiples heads

Revision ID: b9b661c2ba7d
Revises: 67eb4802fe36, ac9a69722ab2
Create Date: 2025-08-04 09:36:20.243845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9b661c2ba7d'
down_revision = ('67eb4802fe36', 'ac9a69722ab2')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
