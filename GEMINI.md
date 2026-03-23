# GEMINI.md - taxcalcindia

This file provides instructional context for Gemini CLI interactions within the `taxcalcindia` project.

## Project Overview
`taxcalcindia` is a lightweight, dependency-free Python package designed to calculate Indian income tax for individuals. It allows users to compute tax under both the "Old" and "New" regimes, providing a comparison and recommendation for the more cost-effective option.

### Core Technologies
- **Language:** Python 3.9+
- **Build System:** `setuptools` (configured in `pyproject.toml`)
- **Testing:** `unittest`
- **Documentation:** Sphinx/ReadTheDocs (configured in `docs/`)

### Architecture
The project is organized into several key modules within the `taxcalcindia/` directory:
- `models.py`: Defines data structures for `TaxSettings`, `SalaryIncome`, `BusinessIncome`, `CapitalGainsIncome`, `OtherIncome`, and `Deductions`. Includes basic validation for non-negative values.
- `slabs.py`: Contains the tax slab definitions for different regimes and age groups.
- `calculator.py`: The core `IncomeTaxCalculator` class that orchestrates the calculation logic, including deductions, surcharges, health and education cess, and regime comparison.
- `exceptions.py`: Custom exceptions for tax-specific calculation errors.

## Building and Running

### Development Environment
To set up the development environment, ensure you have Python 3.9+ installed. It is recommended to use a virtual environment.

```sh
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in editable mode
pip install -e .
```

### Running Tests
The project uses the standard `unittest` framework. All tests are located in the `tests/` directory.

```sh
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run a specific test file
python tests/test_taxcalcindia.py
```

### Building the Package
To build the distribution packages (wheel and sdist):

```sh
# Ensure 'build' is installed
pip install build

# Build the package
python -m build
```

## Development Conventions

### Coding Style
- **Type Hinting:** Use Python 3.9+ type hints for all function signatures and class definitions.
- **Validation:** Use the `_validate_non_negative` helper in `models.py` when adding new numeric fields to models.
- **Naming:** Follow PEP 8 conventions. Refer to `NAMING.md` for project-specific naming context regarding the package name.

### Testing Practices
- **Coverage:** Maintain high test coverage (currently ~91% as per README).
- **Regression Tests:** Always add a new test case in `tests/test_taxcalcindia.py` for any bug fix or new feature.
- **Accuracy:** Tax calculations must be verified against official Income Tax Department of India rules. Use `assert_tax_liability` in tests for consistency.

### Contributions
- Keep changes surgical and focused.
- Ensure all tests pass before submitting a Pull Request.
- Update `example.ipynb` if introducing major API changes or new income/deduction types.

## Key Files
- `taxcalcindia/calculator.py`: Main entry point for calculation logic.
- `taxcalcindia/models.py`: Definitions for all income and deduction inputs.
- `taxcalcindia/slabs.py`: Current tax slabs and rates.
- `tests/test_taxcalcindia.py`: Comprehensive test suite with various taxpayer scenarios.
- `pyproject.toml`: Project metadata and build configuration.
