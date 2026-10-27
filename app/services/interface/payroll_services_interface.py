from abc import ABC,abstractmethod

class PayrollServiceInterface(ABC):

    @abstractmethod
    def calculate_da(self,
         basic_salary: float|int
         )->float|int:
        pass    

    @abstractmethod
    def calculate_pf(self, 
        basic_salary: float|int
        )->float|int:
        pass

    @abstractmethod
    def calculate_gross_salary(self, 
        basic_salary: float|int
        )->float|int:
        pass