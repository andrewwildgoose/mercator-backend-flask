"""increase hash password max length

Revision ID: 003190f70aa4
Revises: 6cb5846991ba
Create Date: 2024-06-14 12:44:02.756873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003190f70aa4'
down_revision = '6cb5846991ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###