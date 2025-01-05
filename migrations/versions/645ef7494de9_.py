"""empty message

Revision ID: 645ef7494de9
Revises: 50ae983991b4
Create Date: 2025-01-04 18:43:58.085132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '645ef7494de9'
down_revision = '50ae983991b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Planet')
    # ### end Alembic commands ###
