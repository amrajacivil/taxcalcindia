"""Models for tax calculation in India"""

from enum import Enum
from .exceptions import TaxCalculationException
from typing import Any

def _validate_non_negative(name: str, value: Any):
    """Normalize None to 0, ensure numeric and non-negative."""
    if value is None:
        return 0
    # allow ints/floats and numeric strings
    if isinstance(value, (int, float)):
        val = value
    else:
        try:
            val = float(value)
        except Exception:
            raise TaxCalculationException(f"{name} must be a number")
    if val < 0:
        raise TaxCalculationException(f"{name} cannot be negative")
    return int(val) if float(val).is_integer() else val


class EmploymentType(Enum):
  """Employment type of the taxpayer.

  Args:
      Enum (str): Description of the employment type.
  """    
  PRIVATE = "private"
  GOVERNMENT = "government"
  SELF_EMPLOYED = "self_employed"


class TaxSettings:
  """Tax settings for an individual taxpayer.
  """  
  def __init__(self, age: int, financial_year: int = 2025, is_metro_resident: bool = True, employment_type: EmploymentType = EmploymentType.PRIVATE):
    """Initialize tax settings for an individual taxpayer.

    Args:
        age (int): Age of the taxpayer.
        financial_year (int): Financial year for tax calculation.
        is_metro_resident (bool, optional): Whether the taxpayer resides in a metro area. Defaults to True.
        employment_type (EmploymentType, optional): Employment type. Defaults to EmploymentType.PRIVATE.

    Raises:
        TaxCalculationException: If the age is invalid.
        TaxCalculationException: If the financial year is not supported.
    """
    self.age = _validate_non_negative("age", age)
    self.financial_year = _validate_non_negative("financial_year", financial_year)
    self.is_metro_resident = is_metro_resident
    self.employment_type = employment_type

    if self.age not in list(range(18,101,1)):
      raise TaxCalculationException("invalid age")
    if self.financial_year not in list(range(2025,2051,1)):
      raise TaxCalculationException("module does not support tax calculation for financial years prior to 2025")

  
class SalaryIncome:
  """Salary income details for the taxpayer.
  """  
  def __init__(self,basic_and_da=0,hra=0,other_allowances=0,bonus_and_commissions=0):
    """Initialize salary income details for the taxpayer.

    Args:
        basic_and_da (int, optional): Basic salary and DA. Defaults to 0.
        hra (int, optional): House Rent Allowance. Defaults to 0.
        other_allowances (int, optional): Other allowances. Defaults to 0.
        bonus_and_commissions (int, optional): Bonus and commissions. Defaults to 0.
    """      
    self.basic_and_da=_validate_non_negative("basic_and_da", basic_and_da)
    self.hra=_validate_non_negative("hra", hra)
    self.other_allowances=_validate_non_negative("other_allowances", other_allowances)
    self.bonus_and_commissions=_validate_non_negative("bonus_and_commissions", bonus_and_commissions)

  @property
  def total(self):
    """Get the total salary income.

    Returns:
        int: The total salary income.
    """    
    return (
        self.basic_and_da
        + self.hra
        + self.other_allowances
        + self.bonus_and_commissions
    )
  
  @property
  def total_eligible_hra(self, settings: TaxSettings): 
      """Get the total eligible HRA for the taxpayer.

      Returns:
          int: The total eligible HRA.
      """
      if settings.is_metro_resident:
          return self.hra * 0.5
      return self.hra * 0.4

class BusinessIncome:
  """Business income details for the taxpayer.
  """  
  def __init__(self,business_income=0,property_income=0):
    """Initialize business income details for the taxpayer.

    Args:
        business_income (int, optional): Business income. Defaults to 0.
        property_income (int, optional): Property income. Defaults to 0.
    """      
    self.business_income=_validate_non_negative("business_income", business_income)
    self.property_income=_validate_non_negative("property_income", property_income)

  @property
  def total(self):
    """Get the total business income.

    Returns:
        int: The total business income.
    """    
    return (
        self.business_income
        + self.property_income
    )
  
class CapitalGainsIncome:
  """Capital gains income details for the taxpayer.
  """  
  def __init__(self, short_term_at_normal = 0, short_term_at_20_percent = 0, long_term_at_12_5_percent = 0, long_term_at_20_percent = 0):
    """Initialize capital gains income details for the taxpayer.

    Args:
        short_term_at_normal (int): Short-term capital gains taxed at normal rates.
        short_term_at_20_percent (int): Short-term capital gains taxed at 20%.
        long_term_at_12_5_percent (int): Long-term capital gains taxed at 12.5%.
        long_term_at_20_percent (int): Long-term capital gains taxed at 20%.
    """
    self.short_term_at_normal = _validate_non_negative("short_term_at_normal", short_term_at_normal)
    self.short_term_at_20_percent = _validate_non_negative("short_term_at_20_percent", short_term_at_20_percent)
    self.long_term_at_12_5_percent = _validate_non_negative("long_term_at_12_5_percent", long_term_at_12_5_percent)
    self.long_term_at_20_percent = _validate_non_negative("long_term_at_20_percent", long_term_at_20_percent)

  @property
  def total(self):
    """Get the total capital gains income.

    Returns:
        int: The total capital gains income.
    """
    return ( 
      self.short_term_at_normal
          + self.short_term_at_20_percent
          + self.long_term_at_12_5_percent
          + self.long_term_at_20_percent
    )

  @property
  def total_capital_gains_tax(self):
    """Calculate the total capital gains tax.

    Returns:
        float: The total capital gains tax.
    """    
    return (
      self.short_term_at_20_percent * 0.2
          + self.long_term_at_12_5_percent * 0.125
          + self.long_term_at_20_percent * 0.2
    )

class OtherIncome:
  """Other income details for the taxpayer.
  """  
  def __init__(self,savings_account_interest=0,fixed_deposit_interest=0,other_sources=0):
    """Initialize other income details for the taxpayer.

    Args:
        savings_account_interest (int, optional): Savings account interest. Defaults to 0.
        fixed_deposit_interest (int, optional): Fixed deposit interest. Defaults to 0.
        other_sources (int, optional): Other sources of income. Defaults to 0.
    """
    self.savings_account_interest=_validate_non_negative("savings_account_interest", savings_account_interest)
    self.fixed_deposit_interest=_validate_non_negative("fixed_deposit_interest", fixed_deposit_interest)
    self.other_sources=_validate_non_negative("other_sources", other_sources)

  @property
  def total(self):
    """Get the total other income.

    Returns:
        int: The total other income.
    """    
    return (
        self.savings_account_interest
        + self.fixed_deposit_interest
        + self.other_sources
    )

class Deductions:
  """Deduction details for the taxpayer.
  """  
  def __init__(self,
               section_80c=0,
               section_80d=0,
               section_80gg=0,
               section_80dd=0,
               section_80ddb=0,
               section_24b=0,
               section_80ccd_1b=0,
               section_80ccd_2=0,
               section_80eea=0,
               section_80u=0,
               section_80eeb=0,
               section_80e=0,
               section_80g_50percent=0,
               section_80g_100percent=0,
               section_80gga=0,
               section_80ggc=0,
               rent_for_hra_exemption=0,
               professional_tax=0,
               food_coupons=0,
               other_exemption=0):
    """
    Deduction details for a taxpayer under the **Old Tax Regime (FY 2024–25 / AY 2025–26)**.

    All amounts should be provided in INR. The calculator will automatically
    apply statutory limits wherever applicable.

    Args:
        section_80c (int, optional):
            Investments and expenses eligible under Section 80C such as EPF, PPF,
            ELSS, Life Insurance Premium, Tuition Fees, Principal repayment of
            home loan, etc.
            Maximum deduction allowed: ₹1,50,000 (combined cap under 80C).

        section_80d (int, optional):
            Health insurance premium paid for self, spouse, children, and parents.
            Includes preventive health check-ups.
            Maximum allowed:
            - ₹25,000 for self/family
            - Additional ₹25,000 for parents
            - Up to ₹50,000 if parents are senior citizens
            Overall cap considered by calculator: ₹1,00,000.

        section_80gg (int, optional):
            Deduction for rent paid when HRA is not received.
            Applicable only if taxpayer, spouse, or minor child does not own
            residential property at the place of employment.
            Actual eligible amount is calculated as per rules (₹5,000 per month max).

        section_80dd (int, optional):
            Deduction for maintenance and medical treatment of a dependent
            with disability.
            - ₹75,000 for normal disability
            - ₹1,25,000 for severe disability (≥80%).

        section_80ddb (int, optional):
            Medical treatment expenses for specified critical illnesses
            for self or dependents.
            Maximum allowed:
            - ₹40,000 (non-senior citizens)
            - ₹1,00,000 (senior citizens).

        section_24b (int, optional):
            Interest paid on home loan for self-occupied property.
            Maximum deduction allowed: ₹2,00,000.

        section_80ccd_1b (int, optional):
            Additional contribution to National Pension System (NPS – Tier I).
            Over and above Section 80C limit.
            Maximum additional deduction: ₹50,000.

        section_80ccd_2 (int, optional):
            Employer’s contribution to NPS.
            Deduction allowed up to 10% of basic salary + DA (14% for government employees).
            This is over and above Section 80C and 80CCD(1B).

        section_80eea (int, optional):
            Interest on home loan for affordable housing (sanctioned before
            31 March 2022).
            Maximum additional deduction: ₹1,50,000.

        section_80u (int, optional):
            Deduction for a resident individual with disability.
            - ₹75,000 for normal disability
            - ₹1,25,000 for severe disability.

        section_80eeb (int, optional):
            Interest paid on loan taken for purchase of an electric vehicle.
            Maximum deduction allowed: ₹1,50,000.

        section_80e (int, optional):
            Interest paid on education loan for higher studies
            (self, spouse, children).
            No upper monetary limit.
            Deduction available for up to 8 consecutive assessment years.

        section_80g_50percent (int, optional):
            Donations made to approved charitable institutions
            eligible for 50% deduction (with or without qualifying limit,
            as applicable).

        section_80g_100percent (int, optional):
            Donations made to approved funds eligible for 100% deduction
            (subject to conditions).

        section_80gga (int, optional):
            Donations for scientific research or rural development.
            No deduction allowed if taxpayer has business/professional income.

        section_80ggc (int, optional):
            Donations made to political parties or electoral trusts.
            No maximum limit, but cash donations are not allowed.

        rent_for_hra_exemption (int, optional):
            Rent paid for claiming HRA exemption.
            Actual exemption is calculated separately based on salary,
            rent paid, and city of residence.

        professional_tax (int, optional):
            Professional tax paid to state government.
            Maximum deduction allowed: ₹2,500.

        food_coupons (int, optional):
            Meal vouchers/food coupons (e.g., Sodexo).
            Tax-exempt up to ₹2,200 per month (₹26,400 annually).

        other_exemption (int, optional):
            Any other exemptions allowed under salary (if applicable).
            No predefined statutory limit.
    """

    self.section_80c=min(_validate_non_negative("section_80c", section_80c),150000)
    self.section_80d=min(_validate_non_negative("section_80d", section_80d), 100000)
    self.section_80gg=_validate_non_negative("section_80gg", section_80gg) # calculated based on settings
    self.section_80dd=min(_validate_non_negative("section_80dd", section_80dd), 1250000)
    self.section_80ddb=_validate_non_negative("section_80ddb", section_80ddb)
    self.section_24b=min(_validate_non_negative("section_24b", section_24b), 200000)
    self.section_80ccd_1b=min(_validate_non_negative("section_80ccd_1b", section_80ccd_1b), 50000)
    self.section_80ccd_2=_validate_non_negative("section_80ccd_2", section_80ccd_2) #TODO: implement logic for section 80CCD(2) based on employer contribution
    self.section_80eea=min(_validate_non_negative("section_80eea", section_80eea), 150000)
    self.section_80u=min(_validate_non_negative("section_80u", section_80u), 125000)
    self.section_80eeb=min(_validate_non_negative("section_80eeb", section_80eeb), 150000)
    self.section_80e=_validate_non_negative("section_80e", section_80e) #no limit
    self.section_80g_50percent=_validate_non_negative("section_80g_50percent", section_80g_50percent) #no limit
    self.section_80g_100percent=_validate_non_negative("section_80g_100percent", section_80g_100percent) #no limit
    self.section_80gga=_validate_non_negative("section_80gga", section_80gga) #no limit
    self.section_80ggc=_validate_non_negative("section_80ggc", section_80ggc) #no limit
    self._section_80tta = 0
    self._section_80ttb = 0
    self.rent_for_hra_exemption=_validate_non_negative("rent_for_hra_exemption", rent_for_hra_exemption) # calculated based on settings
    self.professional_tax=min(_validate_non_negative("professional_tax", professional_tax), 2500)
    self.food_coupons=min(_validate_non_negative("food_coupons", food_coupons), 26400)
    self.other_exemption=_validate_non_negative("other_exemption", other_exemption) #no limit

  
  @property
  def section_80tta(self):
    return self._section_80tta

  @section_80tta.setter
  def section_80tta(self, value):
    """Set section 80TTA value with basic validation (non-negative)."""
    if value is None:
      value = 0
    if value < 0:
      raise TaxCalculationException("section_80tta cannot be negative")
    value = min(value, 10000)
    self._section_80tta = value

  @property
  def section_80ttb(self):
    return self._section_80ttb

  @section_80ttb.setter
  def section_80ttb(self, value):
    """Set section 80TTB value with basic validation (non-negative)."""
    if value is None:
      value = 0
    if value < 0:
      raise TaxCalculationException("section_80ttb cannot be negative")
    value = min(value, 50000)
    self._section_80ttb = value

  @property
  def total(self):
    """Calculate the total deductions.

    Returns:
        int: Total deductions.
    """    
    return (
        self.section_80c
        + self.section_80d
        + self.section_80dd
        + self.section_24b
        + self.section_80ccd_1b
        + self.section_80eea
        + self.section_80u
        + self.section_80eeb
        + self.section_80e
        + self.section_80g_50percent
        + self.section_80g_100percent
        + self.section_80gga
        + self.section_80ggc
        + self.section_80ggc
        + self.section_80tta
        + self.section_80ttb
        + self.professional_tax
        + self.food_coupons
        + self.other_exemption
    )

