# taxcalcindia

A lightweight Python package to calculate Indian income tax for individuals. Designed for local use and packaging on PyPI.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Table of Contents

- [Highlights](#highlights)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Example notebook](#example-notebook)
- [API pointers](#api-pointers)
- [Contributing](#contributing)
- [License](#license)
- [Important notice](#important-notice)
- [Support the project](#support-the-project)

## Highlights

- Compute tax under both the new and old regimes and recommend the cheaper regime.
- Support for salary, business, capital gains and other incomes.
- Common deductions and simple slab lookup.
- Small, well-documented models suitable for packaging and testing.

## Installation

Install from PyPI:

```sh
pip install taxcalcindia
```


## Quick start

Example usage:

```py
from taxcalcindia import IncomeTaxCalculator, TaxSettings, SalaryIncome, Deductions

settings = TaxSettings(age=27, financial_year=2025)
salary = SalaryIncome(basic_and_da=500000, other_allowances=500000, bonus_and_commissions=350000)
deductions = Deductions(food_coupons=26400, professional_tax=2500)

calc = IncomeTaxCalculator(settings=settings, salary=salary, deductions=deductions)
result = calc.calculate_tax(is_comparision_needed=True, is_tax_per_slab_needed=True, display_result=False)

print(result)
```

## Example notebook

A longer, runnable example is provided in the repository: [example.ipynb](example.ipynb). It contains multiple scenarios and is extended based on user requests.

## API pointers

- Main calculator: `taxcalcindia.calculator.IncomeTaxCalculator`
- Input models:
  - EmploymentType (Enum)
  - TaxSettings (age, financial_year, is_metro_resident, employment_type)
  - SalaryIncome (basic_and_da, hra, other_allowances, bonus_and_commissions, total, total_eligible_hra(settings))
  - BusinessIncome (business_income, property_income, total)
  - CapitalGainsIncome (short_term_at_normal, short_term_at_20_percent, long_term_at_12_5_percent, long_term_at_20_percent, total, total_capital_gains_tax)
  - OtherIncome (savings_account_interest, fixed_deposit_interest, other_sources, total)
  - Deductions (section_80c, section_80d, section_80gg, section_24b, section_80ccd_1b, section_80ccd_2, section_80eea, section_80u, section_80eeb, section_80e, section_80g_50percent, section_80g_100percent, section_80gga, section_80ggc, rent_for_hra_exemption, professional_tax, food_coupons, other_exemption, section_80tta, section_80ttb, total)
- Slab retrieval: `taxcalcindia.slabs.get_tax_slabs`
- Package exceptions: `taxcalcindia.exceptions.TaxCalculationException`

## Contributing

Contributions via PRs are welcome. Please:

- Follow standard Python packaging practices.
- Include tests for new features.
- Keep changes small and documented.

## License

MIT — see [LICENSE](LICENSE)

## Important notice

- **Do NOT use this package as the sole source for filing income tax returns. This project is provided as an aid/reference only. Always audit calculations yourself or consult a government-approved tax professional or authorised tax-filing service before submitting returns. The creator is not responsible for any misfiled tax returns or financial/legal consequences arising from using this package.**


## If you find this project useful, A small cup helps a lot!

<a href="https://buymeacoffee.com/amraja" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## More from the developer

Reach out or explore other projects by the developer at: https://amraja.in/


