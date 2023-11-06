"""da schreibe ich meine nachrichten

Revision ID: 808764ad649c
Revises: 
Create Date: 2023-11-03 13:25:02.250953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '808764ad649c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
