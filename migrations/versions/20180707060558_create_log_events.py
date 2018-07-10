"""create_log_events

Revision ID: 0fb70edce740
Revises: 41e5cfd6e54b
Create Date: 2018-07-07 06:058

"""

# revision identifiers, used by Alembic.
revision = '0fb70edce740'
down_revision = '41e5cfd6e54b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;"""))
    op.create_table(
        'log_events',
        sa.Column('id', UUID(), nullable=False, default=uuid.uuid4, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('log_id', UUID(), ForeignKey('logs.id'), nullable=False, index=True),
        sa.Column('drone_id', sa.Integer()),
        sa.Column('drone_generation', sa.Integer()),
        sa.Column('start_time', sa.DateTime()),
        sa.Column('end_time', sa.DateTime()),
        sa.Column('lat', sa.Float(precision=10)),
        sa.Column('lon', sa.Float(precision=10)),
        sa.Column('building_layout_map', sa.String()),
        sa.Column('duration_in_seconds', sa.Integer()),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('log_events')
