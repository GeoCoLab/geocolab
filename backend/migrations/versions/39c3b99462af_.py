"""empty message

Revision ID: 39c3b99462af
Revises: ffcc82c91e82
Create Date: 2022-05-27 16:42:30.437284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39c3b99462af'
down_revision = 'ffcc82c91e82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog_post', sa.Column('posted', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blog_post', 'posted')
    # ### end Alembic commands ###
