"""insert employee details data

Revision ID: 2b05625baf79
Revises: 9ad5469f56e4
Create Date: 2026-10-21 12:15:01.833801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b05625baf79'
down_revision: Union[str, Sequence[str], None] = '9ad5469f56e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
            INSERT INTO employee_deatils
            (employee_id, employee_name, gender, department) VALUES
            (1, 'Arun', 'Male', 'IT'), (2, 'Priya', 'Female', 'HR'), (3, 'Kumar', 'Male', 'IT'),
            (4, 'Divya', 'Female', 'Finance'),(5, 'Ravi', 'Male', 'HR')

        """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM employee_deatils WHERE employee_id IN (1, 2, 3, 4, 5)")
