"""Changes in nullable fields

Revision ID: 71968fc31b62
Revises: 6f1570586510
Create Date: 2020-05-31 16:31:31.335559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71968fc31b62'
down_revision = '6f1570586510'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'desc',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('item', 'image_1',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('item', 'image_2',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('item', 'image_3',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('item', 'image_3',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.alter_column('item', 'image_2',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.alter_column('item', 'image_1',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.alter_column('item', 'desc',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
