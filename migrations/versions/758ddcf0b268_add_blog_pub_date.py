"""add_blog_pub_date

Revision ID: 758ddcf0b268
Revises: 7f562bb9f639
Create Date: 2024-05-07 22:52:55.820687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '758ddcf0b268'
down_revision = '7f562bb9f639'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('image', sa.String(length=256), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('pub_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('text')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog')
    # ### end Alembic commands ###
