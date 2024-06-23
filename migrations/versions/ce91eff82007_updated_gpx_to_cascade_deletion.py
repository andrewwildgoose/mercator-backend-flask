"""Updated gpx to cascade deletion.

Revision ID: ce91eff82007
Revises: 271c13b20981
Create Date: 2024-06-23 16:11:14.440439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce91eff82007'
down_revision = '271c13b20981'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file_shares', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('file_shares_shared_with_user_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('file_shares_gpx_file_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'gpx_files', ['gpx_file_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'user', ['shared_with_user_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('gpx_files', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.create_unique_constraint(None, ['owner_id'])
        batch_op.drop_constraint('gpx_files_owner_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['owner_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('track_points', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('track_points_track_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'tracks', ['track_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('tracks', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('tracks_gpx_file_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'gpx_files', ['gpx_file_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('waypoints', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.drop_constraint('waypoints_gpx_file_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'gpx_files', ['gpx_file_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('waypoints', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('waypoints_gpx_file_id_fkey', 'gpx_files', ['gpx_file_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('tracks', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('tracks_gpx_file_id_fkey', 'gpx_files', ['gpx_file_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('track_points', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('track_points_track_id_fkey', 'tracks', ['track_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('gpx_files', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('gpx_files_owner_id_fkey', 'user', ['owner_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('file_shares', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('file_shares_gpx_file_id_fkey', 'gpx_files', ['gpx_file_id'], ['id'])
        batch_op.create_foreign_key('file_shares_shared_with_user_id_fkey', 'user', ['shared_with_user_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###