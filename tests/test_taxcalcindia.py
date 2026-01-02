import os
import sys
import unittest

# ensure project root is on sys.path so package imports work
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from taxcalcindia.calculator import IncomeTaxCalculator
from taxcalcindia.models import (
    SalaryIncome,
    BusinessIncome,
    OtherIncome,
    Deductions,
    TaxSettings,
    CapitalGainsIncome,
)


def _extract_total(value):
    """
    Helper to extract a numeric tax total from either:
     - a numeric value (float/int) returned as regime tax
     - a dict like {'total': ..., 'surcharge': ..., 'cess': ...}
    """
    if isinstance(value, dict):
        return float(value.get("total", 0.0))
    return float(value)


class TestIncomeTaxCalculator(unittest.TestCase):
    def assert_tax_liability(self, actual, expected_new, expected_old, places=6):
        self.assertIn("tax_liability", actual, "Result must contain 'tax_liability'")
        tax_liab = actual["tax_liability"]

        self.assertIn("new_regime", tax_liab)
        self.assertIn("old_regime", tax_liab)

        new_val = _extract_total(tax_liab["new_regime"])
        old_val = _extract_total(tax_liab["old_regime"])

        self.assertAlmostEqual(new_val, float(expected_new), places=places)
        self.assertAlmostEqual(old_val, float(expected_old), places=places)

    def test_case_1_salary_only_no_hra(self):
        settings = TaxSettings(age=27, financial_year=2025, is_metro_resident=True)
        salary = SalaryIncome(basic_and_da=900000, other_allowances=200000, bonus_and_commissions=25000)

        calc = IncomeTaxCalculator(settings, salary)
        output = calc.calculate_tax(is_comparision_needed=False, is_tax_per_slab_needed=False)

        # Expected: new_regime 0.0, old_regime 140400.0
        self.assert_tax_liability(output, expected_new=0.0, expected_old=140400.0)

    def test_case_2_with_hra_provided(self):
        settings = TaxSettings(age=27, financial_year=2025, is_metro_resident=True)
        salary = SalaryIncome(
            basic_and_da=900000, other_allowances=200000, bonus_and_commissions=25000, hra=500000
        )
        calc = IncomeTaxCalculator(settings, salary)
        output = calc.calculate_tax(is_comparision_needed=False, is_tax_per_slab_needed=False)
        # Expected: new_regime 117000.0, old_regime 296400.0
        self.assert_tax_liability(output, expected_new=117000.0, expected_old=296400.0)

    def test_case_3_full_metadata(self):
        settings = TaxSettings(age=27, financial_year=2025, is_metro_resident=True)
        salary = SalaryIncome(
            basic_and_da=900000, other_allowances=200000, bonus_and_commissions=25000, hra=500000
        )
        deductions = Deductions(rent_for_hra_exemption=450000)
        calc = IncomeTaxCalculator(settings, salary, deductions=deductions)
        output = calc.calculate_tax(is_comparision_needed=True, is_tax_per_slab_needed=True)

        # tax_liability top-level structure
        self.assertIn("tax_liability", output)
        tax_liab = output["tax_liability"]
        self.assertIn("new_regime", tax_liab)
        self.assertIn("old_regime", tax_liab)

        # each regime should be a dict with total, surcharge, cess
        new_reg = tax_liab["new_regime"]
        old_reg = tax_liab["old_regime"]
        for reg in (new_reg, old_reg):
            self.assertIsInstance(reg, dict)
            self.assertIn("total", reg)
            self.assertIn("surcharge", reg)
            self.assertIn("cess", reg)

        # validate numeric values precisely (allowing float conversion)
        self.assertAlmostEqual(float(new_reg.get("total", 0.0)), 117000.0, places=6)
        self.assertAlmostEqual(float(new_reg.get("surcharge", 0.0)), 0.0, places=6)
        self.assertAlmostEqual(float(new_reg.get("cess", 0.0)), 4500.0, places=6)

        self.assertAlmostEqual(float(old_reg.get("total", 0.0)), 184080.0, places=6)
        self.assertAlmostEqual(float(old_reg.get("surcharge", 0.0)), 0.0, places=6)
        self.assertAlmostEqual(float(old_reg.get("cess", 0.0)), 7080.0, places=6)

        # validate comparison metadata
        self.assertIn("tax_regime_comparison", output)
        comp = output["tax_regime_comparison"]
        self.assertIn("recommended_regime", comp)
        self.assertIn("summary", comp)
        self.assertIn("tax_savings_amount", comp)

        self.assertEqual(comp.get("recommended_regime"), "new")
        self.assertEqual(comp.get("tax_savings_amount"), 67080)
        self.assertEqual(
            comp.get("summary"),
            "New tax regime results in a savings of ₹67080 compared to the old regime",
        )

    def test_case_4_tax_per_slabs(self):
        settings = TaxSettings(age=27, financial_year=2025, is_metro_resident=True)
        salary = SalaryIncome(
            basic_and_da=900000, other_allowances=200000, bonus_and_commissions=25000, hra=500000
        )
        capital_gains = CapitalGainsIncome(long_term_at_12_5_percent=25000, long_term_at_20_percent=5000)
        other = OtherIncome(savings_account_interest=35000, fixed_deposit_interest=65000)
        deductions = Deductions(rent_for_hra_exemption=450000)

        calc = IncomeTaxCalculator(
            settings, salary, capital_gains=capital_gains, deductions=deductions, other_income=other
        )
        output = calc.calculate_tax(is_comparision_needed=True, is_tax_per_slab_needed=True)

        self.assertIn("tax_per_slabs", output)
        tax_per_slabs = output["tax_per_slabs"]
        self.assertIn("new_regime", tax_per_slabs)
        self.assertIn("old_regime", tax_per_slabs)

        expected_new = {
            (0.0, 400000): 0.0,
            (400000, 800000): 20000.0,
            (800000, 1200000): 40000.0,
            (1200000, 1600000): 60000.0,
            (1600000, 1650000): 10000.0,
        }
        expected_old = {
            (0.0, 250000): 0.0,
            (250000, 500000): 12500.0,
            (500000, 1000000): 100000.0,
            (1000000, 1305000.0): 91500.0,
        }

        new_slabs = tax_per_slabs["new_regime"]
        old_slabs = tax_per_slabs["old_regime"]

        for slab_range, expected_amount in expected_new.items():
            self.assertIn(slab_range, new_slabs, f"Missing slab {slab_range} in new_regime")
            self.assertAlmostEqual(float(new_slabs[slab_range]), float(expected_amount), places=6)

        for slab_range, expected_amount in expected_old.items():
            self.assertIn(slab_range, old_slabs, f"Missing slab {slab_range} in old_regime")
            self.assertAlmostEqual(float(old_slabs[slab_range]), float(expected_amount), places=6)

    # # Additional small unit tests / edge cases

    def test_zero_income_all_zero(self):
        settings = TaxSettings(age=30, financial_year=2025, is_metro_resident=False)
        salary = SalaryIncome(basic_and_da=0, other_allowances=0, bonus_and_commissions=0)
        calc = IncomeTaxCalculator(settings, salary)
        output = calc.calculate_tax()

        self.assertIn("tax_liability", output)
        new_val = _extract_total(output["tax_liability"]["new_regime"])
        old_val = _extract_total(output["tax_liability"]["old_regime"])
        self.assertEqual(new_val, 0.0)
        self.assertEqual(old_val, 0.0)

    def test_invalid_types_raise_or_handle_gracefully(self):
        settings = TaxSettings(age=30, financial_year=2025, is_metro_resident=False)
        # pass strings instead of numbers to ensure calculator doesn't crash catastrophically
        salary = SalaryIncome(basic_and_da="100000", other_allowances="0", bonus_and_commissions="0")
        calc = IncomeTaxCalculator(settings, salary)
        # either it should raise a TypeError/ValueError or handle conversion; test ensures predictable behavior
        try:
            output = calc.calculate_tax()
        except (TypeError, ValueError):
            raise unittest.SkipTest("Calculator raised on invalid input types; acceptable behavior")
        else:
            self.assertIn("tax_liability", output)
            new_val = _extract_total(output["tax_liability"]["new_regime"])
            old_val = _extract_total(output["tax_liability"]["old_regime"])
            self.assertEqual(new_val, 0.0)
            self.assertEqual(old_val, 0.0)


if __name__ == "__main__":
    unittest.main()