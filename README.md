# taxcalcindia

A small Python package to calculate Indian income tax for individuals.  
Designed for local use and packaging on PyPI.

Features
- Calculate tax under new and old regimes and recommend the cheaper regime.
- Support for salary, business and other incomes, and common deductions.
- Simple, well-documented models and slab lookup.

Installation

From source (recommended for development):
```sh
pip install .
```



Quick usage example
```py
from taxcalcindia import IncomeTaxCalculator, TaxSettings, SalaryIncome, Deductions

settings = TaxSettings(age=27, financial_year=2025)
salary = SalaryIncome(basic_and_da=1400000, other_allowances=400000)
deductions = Deductions(section_80e=1000000)

calc = IncomeTaxCalculator(settings, salary, deductions=deductions)
result = calc.calculate_tax()

print(result)
```

API pointers
- Main calculator class: [`taxcalcindia.calculator.IncomeTaxCalculator`](taxcalcindia/calculator.py)
- Input models: [`taxcalcindia.models.TaxSettings`](taxcalcindia/models.py), [`taxcalcindia.models.SalaryIncome`](taxcalcindia/models.py), [`taxcalcindia.models.Deductions`](taxcalcindia/models.py)
- Slab retrieval: [`taxcalcindia.slabs.get_tax_slabs`](taxcalcindia/slabs.py)
- Package exceptions: [`taxcalcindia.exceptions.TaxCalculationException`](taxcalcindia/exceptions.py)

Development
- Packaging: see [setup.py](setup.py)

License
MIT — see [LICENSE](LICENSE)

Contributing
Contributions via PRs are welcome. Please follow standard Python packaging and include tests for new features.