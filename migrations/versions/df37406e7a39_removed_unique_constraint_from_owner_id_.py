"""Removed unique constraint from owner_id in GpxFile

Revision ID: df37406e7a39
Revises: ce91eff82007
Create Date: 2024-06-23 16:47:58.896726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df37406e7a39'
down_revision = 'ce91eff82007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gpx_files', schema=None) as batch_op:
        batch_op.drop_constraint('gpx_files_owner_id_key', type_='unique')
        batch_op.drop_constraint('gpx_files_owner_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['owner_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('gpx_files', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('gpx_files_owner_id_fkey', 'user', ['owner_id'], ['id'], ondelete='CASCADE')
        batch_op.create_unique_constraint('gpx_files_owner_id_key', ['owner_id'])

    # ### end Alembic commands ###
