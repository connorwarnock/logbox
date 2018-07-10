"""create_logs

Revision ID: 41e5cfd6e54b
Revises:
Create Date: 2018-07-07 06:05

"""

# revision identifiers, used by Alembic.
revision = '41e5cfd6e54b'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;"""))
    op.create_table(
        'logs',
        sa.Column('id', UUID(), nullable=False, default=uuid.uuid4, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('source', sa.String()),
        sa.Column('path', sa.String()),
        sa.Column('ingested', sa.Boolean(), server_default='0', nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('logs')
