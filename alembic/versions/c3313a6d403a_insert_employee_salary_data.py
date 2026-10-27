"""insert employee salary data

Revision ID: c3313a6d403a
Revises: 2b05625baf79
Create Date: 2026-10-21 12:16:29.938376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3313a6d403a'
down_revision: Union[str, Sequence[str], None] = '2b05625baf79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        INSERT INTO employee_salary
        (employee_id, basic_salary, da, pf, gross_salary) VALUES
        (1, 30000, 3000, 3600, 33000),(2, 25000, 2500, 3000, 27500),(3, 40000, 4000, 4800, 44000)

        """ )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM employee_salary WHERE employee_id IN (1, 2, 3)")
