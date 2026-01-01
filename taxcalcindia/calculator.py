from .models import SalaryIncome,CapitalGainsIncome,BusinessIncome,OtherIncome,Deductions,TaxSettings,EmploymentType
from .slabs import get_tax_slabs
import pprint


NEW_REGIME_KEY="new_regime"
OLD_REGIME_GEN_KEY="old_regime_general"
OLD_REGIME_SEN_KEY="old_regime_senior"
OLD_REGIME_SUPER_SEN_KEY="old_regime_super_senior"

NEW_REGIME_STANDARD_DEDUCTION=75000
OLD_REGIME_STANDARD_DEDUCTION=50000

NEW_TAX_REGIME_REBATE_LIMIT=1200000
OLD_TAX_REGIME_REBATE_LIMIT=250000
NEW_TAX_REGIME_REBATE=60000
OLD_TAX_REGIME_REBATE=12500

class IncomeTaxCalculator:
  """Income Tax Calculator for individuals.
  """  
  def __init__(
      self,settings: TaxSettings,
      salary: SalaryIncome | None = None,
      capital_gains: CapitalGainsIncome | None = None,
      business: BusinessIncome | None = None,
      other_income: OtherIncome | None = None,
      deductions: Deductions | None = None
      ):
    """Income Tax Calculator for individuals.

    Args:
        settings (TaxSettings): Tax settings for the individual.
        salary (SalaryIncome | None, optional): Salary income details. Defaults to None.
        capital_gains (CapitalGainsIncome | None, optional): Capital gains income details. Defaults to None.
        business (BusinessIncome | None, optional): Business income details. Defaults to None.
        other_income (OtherIncome | None, optional): Other income details. Defaults to None.
        deductions (Deductions | None, optional): Deduction details. Defaults to None.
    """      
    self._validate_inputs(
        settings, salary, capital_gains, business, other_income, deductions
    )
    self.settings=settings
    self.salary=salary or SalaryIncome()
    self.capital_gains=capital_gains or CapitalGainsIncome()
    self.business=business or BusinessIncome()
    self.other_income=other_income or OtherIncome()
    self.deductions=deductions or Deductions()

  def _validate_inputs(
      self, settings, salary, capital_gains, business, other_income, deductions
      ):
    """Validate input parameters for the tax calculator.

    Args:
        settings (TaxSettings): Tax settings for the individual.
        salary (SalaryIncome | None): Salary income details.
        business (BusinessIncome | None): Business income details.
        other_income (OtherIncome | None): Other income details.
        deductions (Deductions | None): Deduction details.

    Raises:
        TypeError: If any of the input parameters are of the wrong type.
        ValueError: If no income source is provided.
        TypeError: If salary is not a SalaryIncome object.
        TypeError: If capital_gains is not a CapitalGainsIncome object.
        TypeError: If business is not a BusinessIncome object.
        TypeError: If other_income is not an OtherIncome object.
        TypeError: If deductions is not a Deductions object.
    """      
    if not isinstance(settings, TaxSettings):
        raise TypeError("settings must be TaxSettings object")

    if not any([salary,business,other_income]):
      raise ValueError(
          "atleast one income source (salary, business, or other_income) is required"
      )

    if salary and not isinstance(salary, SalaryIncome):
        raise TypeError("salary must be SalaryIncome object")

    if capital_gains and not isinstance(capital_gains, CapitalGainsIncome):
        raise TypeError("capital_gains must be CapitalGainsIncome object")

    if business and not isinstance(business, BusinessIncome):
        raise TypeError("business must be BusinessIncome object")

    if other_income and not isinstance(other_income, OtherIncome):
        raise TypeError("other_income must be OtherIncome object")

    if deductions and not isinstance(deductions, Deductions):
        raise TypeError("deductions must be Deductions object")

  @property
  def gross_income(self):
    """Calculate the gross income from all sources.

    Returns:
        float: The total gross income.
    """    
    return (
        self.salary.total
        + self.business.total
        + self.other_income.total
        + self.capital_gains.total
    )
  
  @property
  def total_deductions(self):
    """Calculate the total deductions for the individual."""
    if self.other_income and hasattr(self.other_income,'savings_account_interest'):
      if self.settings.age>60:
        self.deductions.section_80ttb=self.other_income.savings_account_interest
        self.deductions.section_80tta=0
      else:
        self.deductions.section_80tta=self.other_income.savings_account_interest
        self.deductions.section_80ttb=0
    return (
        self.deductions.total
        + max(self.__calculate_hra_component_for_private(),0)
        + max(self.__calculate_hra_component_for_self_employed(),0)
    )


  def __calculate_hra_component_for_private(self):
    if self.settings.employment_type == EmploymentType.PRIVATE:
      hra = min(self.salary.hra, self.salary.basic_and_da * 0.5,self.deductions.rent_for_hra_exemption-0.1*self.salary.basic_and_da)
      return hra
    return 0

  def __calculate_hra_component_for_self_employed(self):
    if self.settings.employment_type == EmploymentType.SELF_EMPLOYED:
      return min(5000,0.25*self.gross_income,0.1*self.salary.basic_and_da)
    return 0


  def __get_taxable_income(self):
    if self.settings.employment_type==EmploymentType.SELF_EMPLOYED:
      old_regime_taxable_income=max(0, self.gross_income  - self.total_deductions)
      new_regime_taxable_income=max(0, self.gross_income)
      return new_regime_taxable_income, old_regime_taxable_income
    old_regime_taxable_income=max(0, self.gross_income - OLD_REGIME_STANDARD_DEDUCTION - self.total_deductions)
    new_regime_taxable_income=max(0, self.gross_income - NEW_REGIME_STANDARD_DEDUCTION)
    return new_regime_taxable_income, old_regime_taxable_income
  
  def __calculate_surcharge(self, taxable_income, regime_type, tax_amount=0):
    
    ti = float(taxable_income)

    def get_rate(ti_value: float, is_new: bool) -> int:
      if ti_value <= 5000000:
        return 0
      if ti_value <= 10000000:
        return 10
      if ti_value <= 20000000:
        return 15
      if ti_value <= 50000000:
        return 25
      return 25 if is_new else 37

    old_rate = get_rate(ti, is_new=False)
    new_rate = get_rate(ti, is_new=True)

    def calc_amount(rate: int):
      return round(float(tax_amount) * (rate / 100.0), 2)
    
    if regime_type == "old":
      return {
        "rate_percent": old_rate, "amount": calc_amount(old_rate)
      }
    elif regime_type == "new":
      return {
        "rate_percent": new_rate, "amount": calc_amount(new_rate)
      }




  def __calculate_tax_per_slab(self,taxable_income,slab):
    tax = 0.0
    tax_per_slab = {}
    if taxable_income <= 0:
      return tax, tax_per_slab

    remaining = float(taxable_income)
    previous_limit = 0.0
    for limit, rate in slab:
      if remaining <= 0:
        break
      slab_end = limit if limit != float("inf") else taxable_income
      taxable_in_slab = min(slab_end - previous_limit, remaining)
      slab_tax = taxable_in_slab * rate
      tax += slab_tax
      tax_per_slab[(previous_limit, min(slab_end, taxable_income))] = slab_tax
      remaining -= taxable_in_slab
      previous_limit = limit
    return tax, tax_per_slab


  def __compute_regime_tax(self, taxable_income: float, slab, rebate_limit: float, regime_type: str, apply_deduction: float = 0.0):
    """Compute tax, surcharge, and cess for a given regime. Returns a dict with components."""
    if taxable_income > rebate_limit:
      base_tax, tax_per_slab = self.__calculate_tax_per_slab(taxable_income, slab)
    else:
      base_tax, tax_per_slab = 0.0, {}
    if apply_deduction:
      base_tax = max(base_tax - apply_deduction, 0.0)
    base_tax += self.capital_gains.total_capital_gains_tax
    surcharge = self.__calculate_surcharge(taxable_income, regime_type, base_tax) or {"amount": 0.0, "rate_percent": 0}
    surcharge_amount = surcharge.get("amount", 0.0)
    tax_after_surcharge = base_tax + (surcharge_amount if surcharge_amount else 0.0)
    cess = round(tax_after_surcharge * 0.04, 2)
    total_tax = tax_after_surcharge + cess

    return {
      "base_tax": round(base_tax, 2),
      "tax_per_slab": tax_per_slab,
      "surcharge": surcharge,
      "surcharge_amount": round(surcharge_amount, 2),
      "cess": cess,
      "total_tax": round(total_tax, 2)
    }


  def calculate_tax(self, is_comparision_needed: bool = True, is_tax_per_slab_needed: bool = False):
    """Calculate tax based on the individual's income and deductions.

    Args:
        is_comparision_needed (bool, optional): Whether to include tax regime comparison. Defaults to True.
        is_tax_per_slab_needed (bool, optional): Whether to include tax per slab details. Defaults to False.

    Returns:
        dict: A dictionary containing the tax calculation results.
    """
    slabs = get_tax_slabs(self.settings.financial_year, self.settings.age)
    new_taxable, old_taxable = self.__get_taxable_income()
    if self.capital_gains:
      new_taxable -= self.capital_gains.total
      old_taxable -= self.capital_gains.total

    # choose appropriate old-regime slab based on age
    if self.settings.age >= 80:
      old_slab_key = OLD_REGIME_SUPER_SEN_KEY
    elif self.settings.age >= 60:
      old_slab_key = OLD_REGIME_SEN_KEY
    else:
      old_slab_key = OLD_REGIME_GEN_KEY

    # compute new and old regime totals using helper
    new_result = self.__compute_regime_tax(
      taxable_income=new_taxable,
      slab=slabs[NEW_REGIME_KEY],
      rebate_limit=NEW_TAX_REGIME_REBATE_LIMIT,
      regime_type="new",
      apply_deduction=0.0
    )

    old_result = self.__compute_regime_tax(
      taxable_income=old_taxable,
      slab=slabs[old_slab_key],
      rebate_limit=OLD_TAX_REGIME_REBATE_LIMIT,
      regime_type="old",
      apply_deduction=0.0
    )

    # recommendation and savings
    new_tax_total = new_result["total_tax"]
    old_tax_total = old_result["total_tax"]

    if new_tax_total > old_tax_total:
      recommended = "old"
      savings = round(new_tax_total - old_tax_total)
      summary = f"Old tax regime results in a savings of ₹{savings} compared to the new regime"
    else:
      recommended = "new"
      savings = round(old_tax_total - new_tax_total)
      summary = f"New tax regime results in a savings of ₹{savings} compared to the old regime"

    recommendation = {
      "recommended_regime": recommended,
      "summary": summary,
      "tax_savings_amount": savings
    }

    result = {
      "income_summary": {
        "gross_income": self.gross_income,
        "gross_deductions": self.deductions.total,
        "new_regime_taxable_income": new_taxable,
        "old_regime_taxable_income": old_taxable
      },
      "tax_liability": {
        "new_regime": {
          "total":  new_tax_total,
          "surcharge": new_result["surcharge"]["amount"],
          "cess" : new_result["cess"]
        },
        "old_regime": {
          "total": old_tax_total,
          "surcharge": old_result["surcharge"]["amount"],
          "cess" : old_result["cess"]
        }
      }
    }

    if is_comparision_needed:
      result["tax_regime_comparison"] = recommendation

    if is_tax_per_slab_needed:
      result["tax_per_slabs"] = {
        "new_regime": new_result["tax_per_slab"],
        "old_regime": old_result["tax_per_slab"]
      }

    pprint.pprint(result, indent=2, sort_dicts=False)
    return


