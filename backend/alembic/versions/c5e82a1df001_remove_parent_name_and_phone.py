"""remove_parent_name_and_phone_from_students

Revision ID: c5e82a1df001
Revises: b3f3b03f4223
Create Date: 2026-10-09 10:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5e82a1df001'
down_revision: Union[str, Sequence[str], None] = 'b3f3b03f4223'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: drop parent_name and parent_phone from students table."""
    op.drop_column('students', 'parent_name')
    op.drop_column('students', 'parent_phone')


def downgrade() -> None:
    """Downgrade schema: restore parent_name and parent_phone to students table."""
    op.add_column('students', sa.Column('parent_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('students', sa.Column('parent_phone', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
