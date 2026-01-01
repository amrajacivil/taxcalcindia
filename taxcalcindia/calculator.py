from models import SalaryIncome,BusinessIncome,OtherIncome,Deductions,TaxSettings,EmploymentType
from slabs import get_tax_slabs
import pprint


NEW_REGIME_KEY="new_regime"
OLD_REGIME_GEN_KEY="old_regime_general"
OLD_REGIME_SEN_KEY="old_regime_senior"
OLD_REGIME_SUPER_SEN_KEY="old_regime_super_senior"

class IncomeTaxCalculator:
  """Income Tax Calculator for individuals.
  """  
  def __init__(
      self,settings: TaxSettings,
      salary: SalaryIncome | None = None,
      business: BusinessIncome | None = None,
      other_income: OtherIncome | None = None,
      deductions: Deductions | None = None
      ):
    """Income Tax Calculator for individuals.

    Args:
        settings (TaxSettings): Tax settings for the individual.
        salary (SalaryIncome | None, optional): Salary income details. Defaults to None.
        business (BusinessIncome | None, optional): Business income details. Defaults to None.
        other_income (OtherIncome | None, optional): Other income details. Defaults to None.
        deductions (Deductions | None, optional): Deduction details. Defaults to None.
    """      
    self._validate_inputs(
        settings, salary, business, other_income, deductions
    )
    self.settings=settings
    self.salary=salary or SalaryIncome()
    self.business=business or BusinessIncome()
    self.other_income=other_income or OtherIncome()
    self.deductions=deductions or Deductions()

  def _validate_inputs(
      self, settings, salary, business, other_income, deductions
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
    )
  
  @property
  def total_deductions(self):
    """Calculate the total deductions for the individual."""
    return (
        self.deductions.total
        + self.__calculate_hra_component_for_private()
        + self.__calculate_hra_component_for_self_employed()
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


  def get_taxable_income(self):
    standard_deduction=self.settings.standard_deduction
    if self.settings.employment_type==EmploymentType.SELF_EMPLOYED:
      standard_deduction=0

    old_regime_taxable_income=max(0, self.gross_income - standard_deduction - self.total_deductions)
    new_regime_taxable_income=max(0, self.gross_income - standard_deduction)
    return new_regime_taxable_income, old_regime_taxable_income

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


  def calculate_tax(self,is_comparision_needed: bool = True, is_tax_per_slab_needed:bool = False):
    """Compute tax for new and old regimes, return a concise comparison and optional slab breakdown.

    Keeps behaviour compatible with previous implementation (old-regime deduction applied using
    self.deductions.total). Outputs are printed with pprint and returned as a dict.
    """
    slabs = get_tax_slabs(self.settings.financial_year, self.settings.age)

    # taxable incomes (function returns new_regime_taxable_income, old_regime_taxable_income)
    new_taxable, old_taxable = self.get_taxable_income()

    # new regime tax
    new_tax, new_tax_per_slab = self.__calculate_tax_per_slab(new_taxable, slabs[NEW_REGIME_KEY])

    # pick appropriate old-regime slab based on age
    if self.settings.age >= 80:
      old_slab_key = OLD_REGIME_SUPER_SEN_KEY
    elif self.settings.age >= 60:
      old_slab_key = OLD_REGIME_SEN_KEY
    else:
      old_slab_key = OLD_REGIME_GEN_KEY

    old_tax, old_tax_per_slab = self.__calculate_tax_per_slab(old_taxable, slabs[old_slab_key])

    # apply deductions to old regime (match previous behaviour)
    old_tax = max(old_tax - self.deductions.total, 0)

    # determine recommendation and savings
    if new_tax > old_tax:
      recommended = "old"
      savings = round(new_tax - old_tax)
      summary = f"Old tax regime results in a savings of ₹{savings} compared to the new regime"
    else:
      recommended = "new"
      savings = round(old_tax - new_tax)
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
        "new_regime": round(new_tax, 2),
        "old_regime": round(old_tax, 2)
      }
    }

    if is_comparision_needed:
      result["tax_regime_comparison"] = recommendation

    if is_tax_per_slab_needed:
      result["tax_per_slabs"] = {
        "new_regime": new_tax_per_slab,
        "old_regime": old_tax_per_slab
      }

    pprint.pprint(result, indent=2, sort_dicts=False)
    return result


