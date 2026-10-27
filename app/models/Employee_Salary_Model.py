from typing import TYPE_CHECKING

from sqlalchemy import (Integer,
                        Numeric , 
                        CheckConstraint,
                        ForeignKey)

from sqlalchemy.orm import Mapped , mapped_column, relationship 
from decimal import Decimal

from app.models.Table_Model import Base


if TYPE_CHECKING:
    from models.Employee_Details_Model import EmployeeDeatils

class EmployeePayDeatils(Base) :

    __tablename__ = "employee_salary"

    __table_args__ = ( 
       
        CheckConstraint("basic_salary>5000",
                        name="ck_basic_salary"),

        CheckConstraint("da>0",
                        name="ck_positive_da"),

        CheckConstraint("pf>0",
                        name="ck_positive_pf"),

        CheckConstraint("gross_salary>basic_salary",
                        name="ck_gross_higher_than_base")
                        
    )

    employee_id: Mapped[int] =  mapped_column( Integer ,
                                              ForeignKey("employee_deatils.employee_id", ondelete="CASCADE"),
                                              primary_key= True )

    basic_salary: Mapped[Decimal] = mapped_column (Numeric(12,2),
                                                   nullable=False)

    da:Mapped[Decimal] = mapped_column (Numeric(12,2),
                                        nullable=False)

    pf:Mapped[Decimal]=mapped_column (Numeric(12,2),
                                    nullable=False)

    gross_salary:Mapped[Decimal]=mapped_column(Numeric(12,2),
                                               nullable=False)
    
    employee :Mapped["EmployeeDeatils"] = relationship( back_populates="salary")
    

    
    