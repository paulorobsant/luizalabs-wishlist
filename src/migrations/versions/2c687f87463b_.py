"""empty message

Revision ID: 2c687f87463b
Revises: 3bca86757f2e
Create Date: 2021-05-19 15:13:51.392391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c687f87463b'
down_revision = '3bca86757f2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('match', sa.Column('latest_alert', sa.DateTime(), nullable=True))
    op.drop_constraint('match_mentor_id_fkey', 'match', type_='foreignkey')
    op.drop_constraint('match_learner_id_fkey', 'match', type_='foreignkey')
    op.create_foreign_key(None, 'match', 'user', ['mentor_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'match', 'user', ['learner_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('match_request_user_id_fkey', 'match_request', type_='foreignkey')
    op.create_foreign_key(None, 'match_request', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('user_company_user_id_fkey', 'user_company', type_='foreignkey')
    op.drop_constraint('user_company_company_id_fkey', 'user_company', type_='foreignkey')
    op.create_foreign_key(None, 'user_company', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'user_company', 'company', ['company_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('user_profile_user_id_fkey', 'user_profile', type_='foreignkey')
    op.create_foreign_key(None, 'user_profile', 'user', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('user_login_attempts_log_owner_id_fkey', 'user_login_attempts_log', schema='logs', type_='foreignkey')
    op.create_foreign_key(None, 'user_login_attempts_log', 'user', ['owner_id'], ['id'], source_schema='logs', referent_schema='public')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_login_attempts_log', schema='logs', type_='foreignkey')
    op.create_foreign_key('user_login_attempts_log_owner_id_fkey', 'user_login_attempts_log', 'user', ['owner_id'], ['id'], source_schema='logs')
    op.drop_constraint(None, 'user_profile', schema='public', type_='foreignkey')
    op.create_foreign_key('user_profile_user_id_fkey', 'user_profile', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'user_company', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'user_company', schema='public', type_='foreignkey')
    op.create_foreign_key('user_company_company_id_fkey', 'user_company', 'company', ['company_id'], ['id'])
    op.create_foreign_key('user_company_user_id_fkey', 'user_company', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'match_request', schema='public', type_='foreignkey')
    op.create_foreign_key('match_request_user_id_fkey', 'match_request', 'user', ['user_id'], ['id'])
    op.drop_constraint(None, 'match', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'match', schema='public', type_='foreignkey')
    op.create_foreign_key('match_learner_id_fkey', 'match', 'user', ['learner_id'], ['id'])
    op.create_foreign_key('match_mentor_id_fkey', 'match', 'user', ['mentor_id'], ['id'])
    op.drop_column('match', 'latest_alert')
    # ### end Alembic commands ###