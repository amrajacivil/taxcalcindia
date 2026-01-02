import os
import sys
import unittest

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
   - a dict like {'total': ..., 'components': {...}}
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

    # each regime should be a dict with total and components containing surcharge and cess
    new_reg = tax_liab["new_regime"]
    old_reg = tax_liab["old_regime"]
    for reg in (new_reg, old_reg):
      self.assertIsInstance(reg, dict)
      self.assertIn("total", reg)
      self.assertIn("components", reg)
      comps = reg["components"]
      self.assertIn("initial_tax", comps)
      self.assertIn("surcharge", comps)
      self.assertIn("cess", comps)

    # validate numeric values precisely (allowing float conversion)
    self.assertAlmostEqual(float(new_reg.get("total", 0.0)), 117000.0, places=6)
    self.assertAlmostEqual(float(new_reg["components"].get("surcharge", 0.0)), 0.0, places=6)
    self.assertAlmostEqual(float(new_reg["components"].get("cess", 0.0)), 4500.0, places=6)

    self.assertAlmostEqual(float(old_reg.get("total", 0.0)), 184080.0, places=6)
    self.assertAlmostEqual(float(old_reg["components"].get("surcharge", 0.0)), 0.0, places=6)
    self.assertAlmostEqual(float(old_reg["components"].get("cess", 0.0)), 7080.0, places=6)

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
      '(0.0, 400000)': 0.0,
      '(400000, 800000)': 20000.0,
      '(800000, 1200000)': 40000.0,
      '(1200000, 1600000)': 60000.0,
      '(1600000, 1650000)': 10000.0,
    }
    expected_old = {
      '(0.0, 250000)': 0.0,
      '(250000, 500000)': 12500.0,
      '(500000, 1000000)': 100000.0,
      '(1000000, 1305000)': 91500.0,
    }

    new_slabs = tax_per_slabs["new_regime"]
    old_slabs = tax_per_slabs["old_regime"]

    def _to_range_tuple(key):
      if isinstance(key, (tuple, list)):
        return (float(key[0]), float(key[1]))
      if isinstance(key, str):
        s = key.strip()
        if s.startswith("(") and s.endswith(")"):
          s = s[1:-1]
        parts = [p.strip() for p in s.split(",")]
        return (float(parts[0]), float(parts[1]))
      try:
        val = ast.literal_eval(str(key))
        return (float(val[0]), float(val[1]))
      except Exception:
        raise ValueError(f"Unsupported slab key format: {key}")

    def _normalize_slabs(slabs_dict):
      norm = {}
      for k, v in slabs_dict.items():
        rng = _to_range_tuple(k)
        norm[rng] = float(v)
      return norm

    norm_new = _normalize_slabs(new_slabs)
    norm_old = _normalize_slabs(old_slabs)

    def _parse_expected_key(s):
      return _to_range_tuple(s)

    def _find_matching_range(norm_dict, target_range, tol=1e-6):
      for k in norm_dict.keys():
        if abs(k[0] - target_range[0]) <= tol and abs(k[1] - target_range[1]) <= tol:
          return k
      return None

    for slab_range_str, expected_amount in expected_new.items():
      rng = _parse_expected_key(slab_range_str)
      match = _find_matching_range(norm_new, rng)
      self.assertIsNotNone(match, f"Missing slab {slab_range_str} in new_regime; available: {list(norm_new.keys())}")
      self.assertAlmostEqual(float(norm_new[match]), float(expected_amount), places=6)

    for slab_range_str, expected_amount in expected_old.items():
      rng = _parse_expected_key(slab_range_str)
      match = _find_matching_range(norm_old, rng)
      self.assertIsNotNone(match, f"Missing slab {slab_range_str} in old_regime; available: {list(norm_old.keys())}")
      self.assertAlmostEqual(float(norm_old[match]), float(expected_amount), places=6)

  def test_case_5_senior_citizen_business_capital_gains(self):
    settings = TaxSettings(age=63, financial_year=2025)
    business = BusinessIncome(business_income=800000)
    capital_gains = CapitalGainsIncome(short_term_at_20_percent=200000, long_term_at_12_5_percent=350000)
    other_income = OtherIncome(savings_account_interest=200000, fixed_deposit_interest=150000)
    deductions = Deductions(section_80c=250000, section_80d=150000)

    calc = IncomeTaxCalculator(
      settings=settings,
      business=business,
      capital_gains=capital_gains,
      other_income=other_income,
      deductions=deductions,
    )
    output = calc.calculate_tax(is_comparision_needed=True, is_tax_per_slab_needed=True, display_result=False)

    # income summary validations
    self.assertIn("income_summary", output)
    inc = output["income_summary"]
    self.assertAlmostEqual(float(inc.get("gross_income", 0.0)), 1700000.0)
    self.assertAlmostEqual(float(inc.get("gross_deductions", 0.0)), 300000.0)
    self.assertAlmostEqual(float(inc.get("new_regime_taxable_income", 0.0)), 1700000.0)
    self.assertAlmostEqual(float(inc.get("old_regime_taxable_income", 0.0)), 1400000.0)

    # tax liability validations
    self.assertIn("tax_liability", output)
    tax_liab = output["tax_liability"]
    self.assertIn("new_regime", tax_liab)
    self.assertIn("old_regime", tax_liab)

    new_reg = tax_liab["new_regime"]
    old_reg = tax_liab["old_regime"]
    for reg in (new_reg, old_reg):
      self.assertIsInstance(reg, dict)
      self.assertIn("total", reg)
      self.assertIn("components", reg)
      comps = reg["components"]
      self.assertIn("initial_tax", comps)
      self.assertIn("surcharge", comps)
      self.assertIn("cess", comps)

    self.assertAlmostEqual(float(new_reg.get("total", 0.0)), 144300.0)
    self.assertAlmostEqual(float(new_reg["components"].get("surcharge", 0.0)), 0.0)
    self.assertAlmostEqual(float(new_reg["components"].get("cess", 0.0)), 5550.0)
    self.assertAlmostEqual(float(old_reg.get("total", 0.0)), 170300.0)
    self.assertAlmostEqual(float(old_reg["components"].get("surcharge", 0.0)), 0.0)
    self.assertAlmostEqual(float(old_reg["components"].get("cess", 0.0)), 6550.0)

    # comparison metadata
    self.assertIn("tax_regime_comparison", output)
    comp = output["tax_regime_comparison"]
    self.assertEqual(comp.get("recommended_regime"), "new")
    self.assertEqual(comp.get("tax_savings_amount"), 26000)
    self.assertEqual(
      comp.get("summary"),
      "New tax regime results in a savings of ₹26000 compared to the old regime",
    )
  
  def test_case_6_high_income_hra_and_deductions(self):
    settings = TaxSettings(age=50, financial_year=2025, is_metro_resident=True)
    salary = SalaryIncome(
      basic_and_da=7000000,
      other_allowances=750000,
      bonus_and_commissions=3000000,
      hra=6000000,
    )
    other_income = OtherIncome(savings_account_interest=500000, other_sources=250000)
    deductions = Deductions(
      section_80c=250000,
      rent_for_hra_exemption=4500000,
      professional_tax=2500,
      section_80d=800000,
      section_24b=700000,
    )

    calc = IncomeTaxCalculator(settings, salary, deductions=deductions, other_income=other_income)
    output = calc.calculate_tax(is_comparision_needed=True, is_tax_per_slab_needed=True, display_result=False)

    # income summary assertions
    self.assertIn("income_summary", output)
    inc = output["income_summary"]
    self.assertAlmostEqual(float(inc.get("gross_income", 0.0)), 17500000.0)
    self.assertAlmostEqual(float(inc.get("gross_deductions", 0.0)), 462500.0)
    self.assertAlmostEqual(float(inc.get("new_regime_taxable_income", 0.0)), 17425000.0)
    self.assertAlmostEqual(float(inc.get("old_regime_taxable_income", 0.0)), 13487500.0)

    # tax liability assertions
    self.assertIn("tax_liability", output)
    tax_liab = output["tax_liability"]
    self.assertIn("new_regime", tax_liab)
    self.assertIn("old_regime", tax_liab)

    new_reg = tax_liab["new_regime"]
    old_reg = tax_liab["old_regime"]
    for reg in (new_reg, old_reg):
      self.assertIsInstance(reg, dict)
      self.assertIn("total", reg)
      self.assertIn("components", reg)
      comps = reg["components"]
      self.assertIn("initial_tax", comps)
      self.assertIn("surcharge", comps)
      self.assertIn("cess", comps)

    self.assertAlmostEqual(float(new_reg.get("total", 0.0)), 5749770.0)
    self.assertAlmostEqual(float(new_reg["components"].get("initial_tax", 0.0)), 4807500.0)
    self.assertAlmostEqual(float(new_reg["components"].get("surcharge", 0.0)), 721125.0)
    self.assertAlmostEqual(float(new_reg["components"].get("cess", 0.0)), 221145.0)

    self.assertAlmostEqual(float(old_reg.get("total", 0.0)), 4615065.0)
    self.assertAlmostEqual(float(old_reg["components"].get("initial_tax", 0.0)), 3858750.0)
    self.assertAlmostEqual(float(old_reg["components"].get("surcharge", 0.0)), 578812.5)
    self.assertAlmostEqual(float(old_reg["components"].get("cess", 0.0)), 177502.5)

    # comparison metadata
    self.assertIn("tax_regime_comparison", output)
    comp = output["tax_regime_comparison"]
    self.assertEqual(comp.get("recommended_regime"), "old")
    self.assertEqual(comp.get("tax_savings_amount"), 1134705)
    self.assertEqual(
      comp.get("summary"),
      "Old tax regime results in a savings of ₹1134705 compared to the new regime",
    )

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