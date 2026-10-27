from typing import TYPE_CHECKING,Optional

from sqlalchemy import (Integer,
                        String)

from sqlalchemy.orm import Mapped , mapped_column , relationship

from app.models.Table_Model import Base


if TYPE_CHECKING:
    from models.Employee_Salary_Model import EmployeePayDeatils

class EmployeeDeatils(Base):
    __tablename__ = "employee_deatils"


    employee_id : Mapped[int] = mapped_column(Integer,
                                            primary_key=True)

    employee_name :Mapped[str] = mapped_column(String(50),
                                               nullable=False)

    gender : Mapped[str] = mapped_column(String(7),
                                         nullable=False)

    department : Mapped[str] = mapped_column(String(10),
                                             nullable=False)

    salary :Mapped[Optional["EmployeePayDeatils"]] = relationship( back_populates="employee", uselist=False)