Usage
=====

Basic usage example::

    from taxcalcindia.calculator import IncomeTaxCalculator
    from taxcalcindia.models import (
        SalaryIncome,
        BusinessIncome,
        OtherIncome,
        Deductions,
        TaxSettings,
        CapitalGainsIncome,
        EmploymentType
    )
    settings = TaxSettings(age=27, financial_year=2025, is_metro_resident=True)
    salary = SalaryIncome(basic_and_da=500000, other_allowances=500000, bonus_and_commissions=350000)
    deductions = Deductions(food_coupons=26400, professional_tax=2500)

    calc = IncomeTaxCalculator(settings=settings, salary=salary, deductions=deductions)
    calculated_tax = calc.calculate_tax(is_tax_per_slab_needed=True)  
    calculated_tax

