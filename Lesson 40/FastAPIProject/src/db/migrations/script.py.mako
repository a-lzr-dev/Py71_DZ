"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}
#    user_table = table('users',
#        column('id', sa.Integer),
#        column('username', sa.String),
#        column('password', sa.String),
#        column('email', sa.String),
#        column('is_admin', sa.Boolean)
#    )
#    op.bulk_insert(user_table,
#        [
#            {'username': 'Admin', 'email': 'admin@example.com', 'is_admin': 1},
#            {'username': 'Test', 'email': 'test@example.com', 'is_admin': 0},
#        ]
#    )


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}
#    op.execute("DELETE FROM users WHERE email IN ('admin@example.com', 'test@example.com')")