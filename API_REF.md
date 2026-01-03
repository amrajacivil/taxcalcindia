# IncomeTaxCalculator – Public API Reference

This document lists all public functions and cheap getters exposed by  
`taxcalcindia.calculator.IncomeTaxCalculator`, along with their intended usage.

---

## Main Calculator

- **Class:** `taxcalcindia.calculator.IncomeTaxCalculator`

---

## Core Function

### calculate_tax() -> dict

Performs the complete income tax computation and returns a detailed structured
dictionary containing income summary, tax liability, regime comparison, and
optional slab-wise tax details.

Usage:

    calc.calculate_tax(
        is_comparision_needed=True,
        is_tax_per_slab_needed=False,
        display_result=False
    )

---

## Cheap Getters – Tax Liability

### new_regime_tax (property)

Returns the total tax payable under the new tax regime.

Usage:

    calc.new_regime_tax

---

### old_regime_tax (property)

Returns the total tax payable under the old tax regime.

Usage:

    calc.old_regime_tax

---

## Cheap Getters – Taxable Income

### new_regime_taxable_income (property)

Returns taxable income under the new tax regime.

Usage:

    calc.new_regime_taxable_income

---

### old_regime_taxable_income (property)

Returns taxable income under the old tax regime.

Usage:

    calc.old_regime_taxable_income

---

## Cheap Getters – Regime Comparison

### recommended_regime (property)

Returns the recommended tax regime ("new" or "old").

Usage:

    calc.recommended_regime

---

### tax_savings() (method)

Returns tax savings when choosing the recommended regime.

Usage:

    calc.tax_savings()

---

## Tax Breakdown APIs

### new_regime_breakup() (method)

Returns tax components (initial tax, surcharge, cess) under the new tax regime.

Usage:

    calc.new_regime_breakup()

---

### old_regime_breakup() (method)

Returns tax components (initial tax, surcharge, cess) under the old tax regime.

Usage:

    calc.old_regime_breakup()

---

## Tax Slab Details

### tax_per_slab(regime: str = "new") -> dict

Returns slab-wise tax calculation for the specified regime.

Usage:

    calc.tax_per_slab("new")
    calc.tax_per_slab("old")

---

## Example Usage

    from taxcalcindia.calculator import IncomeTaxCalculator

    calc = IncomeTaxCalculator(
        settings=settings,
        salary=salary,
        deductions=deductions
    )

    print(calc.new_regime_tax)
    print(calc.old_regime_tax)
    print(calc.recommended_regime)
    print(calc.tax_savings())

---

## Usage Guidelines

- Prefer cheap getters for quick access
- Use calculate_tax() for full reports
- All getters are cached and do not recompute tax
