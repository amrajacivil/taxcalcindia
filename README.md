# taxcalcindia

A lightweight Python package to calculate Indian income tax for individuals. Designed for local use and packaging on PyPI.

![PyPI - Downloads](https://img.shields.io/pypi/dm/taxcalcindia?color=darkgreen) ![GitHub License](https://img.shields.io/github/license/amrajacivil/taxcalcindia?color=darkgreen) ![PyPI - Status](https://img.shields.io/pypi/status/taxcalcindia) 

![Release](https://img.shields.io/badge/release-automated-blue) ![CI](https://img.shields.io/github/actions/workflow/status/amrajacivil/taxcalcindia/release.yaml?label=CI%2FCD) ![PR Approval](https://img.shields.io/badge/PR%20Approval-required-orange) ![Code Quality](https://img.shields.io/badge/quality-high-success) 


![GitHub tag (with filter)](https://img.shields.io/github/v/tag/amrajacivil/taxcalcindia) ![Static Badge](https://img.shields.io/badge/coverage-91%25-blue) ![Static Badge](https://img.shields.io/badge/covered_lines_of_code-618-blue) ![PyPI - Version](https://img.shields.io/pypi/v/taxcalcindia)



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

## API Documentation

Detailed documentation is available at: https://taxcalcindia.readthedocs.io/en/latest/index.html. The documentation site provides downloadable formats — you can download the docs as PDF or EPUB from the Read the Docs site.

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

A longer, runnable example is provided in the repository: [example.ipynb](https://github.com/amrajacivil/taxcalcindia). It contains multiple scenarios and is extended based on user requests.



## Contributing

Contributions via PRs are welcome. Please:

- Follow standard Python packaging practices.
- Include tests for new features.
- Keep changes small and documented.

## License

MIT — see [LICENSE](https://github.com/amrajacivil/taxcalcindia)

## Important notice

- **Do NOT use this package as the sole source for filing income tax returns. This project is provided as an aid/reference only. Always audit calculations yourself or consult a government-approved tax professional or authorised tax-filing service before submitting returns. The creator is not responsible for any misfiled tax returns or financial/legal consequences arising from using this package.**

### Package Naming and trademark

A brief trademark check for the package name is recorded in [NAMING.md](./NAMING.md). The name "taxcalcindia" was searched on the Government of India Registered Trademark site and, at the time of this release, no registrations were found. This information is provided for reference only and does not constitute legal advice.


## If you find this project useful, A small cup helps a lot!

<a href="https://buymeacoffee.com/amraja" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## More from the developer

Reach out or explore other projects by the developer at: https://amraja.in/


If any link in this README does not redirect or returns "Not Found", please locate the referenced document in the parent GitHub repository: https://github.com/amrajacivil/taxcalcindia


