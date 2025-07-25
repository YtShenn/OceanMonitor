"""empty message

Revision ID: a7b19024ec47
Revises: 
Create Date: 2024-06-13 22:33:25.217852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b19024ec47'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('edit_content', sa.String(length=128), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update_record', schema=None) as batch_op:
        batch_op.drop_column('edit_content')

    # ### end Alembic commands ###
