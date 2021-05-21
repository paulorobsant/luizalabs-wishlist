"""empty message

Revision ID: 3bca86757f2e
Revises: 
Create Date: 2021-05-16 12:23:37.680516

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3bca86757f2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('email_suffixes', postgresql.ARRAY(sa.String()), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('match_term',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('label', sa.String(length=128), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value'),
    schema='public'
    )
    op.create_index(op.f('ix_public_match_term_label'), 'match_term', ['label'], unique=True, schema='public')
    op.create_table('match_training',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('total_prev_entries', sa.Integer(), nullable=False),
    sa.Column('total_new_entries', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('phone_number', sa.String(length=128), nullable=True),
    sa.Column('surname', sa.String(length=128), nullable=True),
    sa.Column('hashed_password', sa.String(length=512), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('email_confirmation_code', sa.String(length=512), nullable=True),
    sa.Column('password_reset_code', sa.String(length=512), nullable=True),
    sa.Column('access_failed_count', sa.Integer(), nullable=False),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('user_invitation',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.Column('code', sa.String(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('user_login_attempts_log',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('browser_info', sa.String(length=512), nullable=True),
    sa.Column('client_ip_address', sa.String(length=18), nullable=False),
    sa.Column('client_name', sa.String(length=512), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.Column('email_or_username', sa.String(length=512), nullable=True),
    sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='logs'
    )
    op.create_table('match',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'FINISHED', 'CANCELLED', 'IN_PROGRESS', name='matchstatus'), nullable=False),
    sa.Column('current_step', postgresql.ENUM('AWAITING_FOR_MENTOR_ACCEPTANCE', 'AWAITING_FOR_LEARNER_ACCEPTANCE', 'MENTOR_SUGGEST_SCHEDULING', 'LEARNER_SUGGEST_SCHEDULING', 'MENTOR_CONFIRM_SCHEDULING', 'LEARNER_CONFIRM_SCHEDULING', 'SCHEDULING_CONFIRMED', 'IN_PROGRESS', name='matchstep'), nullable=False),
    sa.Column('mentor_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('learner_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.ForeignKeyConstraint(['learner_id'], ['public.user.id'], ),
    sa.ForeignKeyConstraint(['mentor_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('match_request',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'FINISHED', 'CANCELLED', 'OVERFLOWED', name='matchrequeststatus'), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('priority', sa.INTEGER(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('user_company',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['public.company.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('user_profile',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('expertises', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('challenges', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('total_conn_as_mentor', sa.Integer(), nullable=False),
    sa.Column('total_conn_as_learner', sa.Integer(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['public.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profile', schema='public')
    op.drop_table('user_company', schema='public')
    op.drop_table('match_request', schema='public')
    op.drop_table('match', schema='public')
    op.drop_table('user_login_attempts_log', schema='logs')
    op.drop_table('user_invitation', schema='public')
    op.drop_table('user', schema='public')
    op.drop_table('match_training', schema='public')
    op.drop_index(op.f('ix_public_match_term_label'), table_name='match_term', schema='public')
    op.drop_table('match_term', schema='public')
    op.drop_table('company', schema='public')
    # ### end Alembic commands ###
