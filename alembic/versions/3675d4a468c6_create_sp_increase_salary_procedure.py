"""create sp_increase_salary procedure

Revision ID: 3675d4a468c6
Revises: c3313a6d403a
Create Date: 2026-10-21 12:20:33.360508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3675d4a468c6'
down_revision: Union[str, Sequence[str], None] = 'c3313a6d403a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
            CREATE OR REPLACE PROCEDURE sp_increase_salary(
                p_employee_id INTEGER,
                p_percent NUMERIC
            )
            LANGUAGE plpgsql
            AS $$
            DECLARE
                v_new_basic NUMERIC(12,2);
                v_da NUMERIC(12,2);
                v_pf NUMERIC(12,2);
            BEGIN
                SELECT ROUND(basic_salary + (basic_salary * p_percent / 100), 2)
                INTO v_new_basic
                FROM employee_salary
                WHERE employee_id = p_employee_id;

                v_da := ROUND(v_new_basic * 0.10, 2);
                v_pf := ROUND(v_new_basic * 0.12, 2);

                UPDATE employee_salary
                SET basic_salary = v_new_basic,
                    da = v_da,
                    pf = v_pf,
                    gross_salary = v_new_basic + v_da + v_pf
                WHERE employee_id = p_employee_id;
            END;
            $$;
        """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP PROCEDURE IF EXISTS sp_increase_salary(INTEGER, NUMERIC)")
