

from app.services.interface.payroll_services_interface import PayrollServiceInterface


class PayrollService(PayrollServiceInterface):
    
    def calculate_da(self,
        basic_salary: float|int
        )->float|int:
        
        return round(basic_salary * 0.10,2)
    
    
    def calculate_pf(self, 
        basic_salary: float|int
        )->float|int:

        return round(basic_salary * 0.12,2)


    def calculate_gross_salary(self, 
        basic_salary: float|int
        )->float|int:
        
        da = self.calculate_da(basic_salary)
        return round(basic_salary + da,2)

    