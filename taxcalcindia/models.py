"""Models for tax calculation in India"""

from enum import Enum
from .exceptions import TaxCalculationException


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
  def __init__(self, age: int, financial_year: int, is_metro_resident: bool = True, employment_type: EmploymentType = EmploymentType.PRIVATE):
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
    self.age = age
    self.financial_year = financial_year
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
    self.basic_and_da=basic_and_da
    self.hra=hra
    self.other_allowances=other_allowances
    self.bonus_and_commissions=bonus_and_commissions

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
    self.business_income=business_income
    self.property_income=property_income

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
    self.short_term_at_normal = short_term_at_normal
    self.short_term_at_20_percent = short_term_at_20_percent
    self.long_term_at_12_5_percent = long_term_at_12_5_percent
    self.long_term_at_20_percent = long_term_at_20_percent

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
    self.savings_account_interest=savings_account_interest
    self.fixed_deposit_interest=fixed_deposit_interest
    self.other_sources=other_sources

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
    """Deduction details for the taxpayer.

    Args:
        section_80c (int, optional): Section 80C deductions. Defaults to 0.
        section_80d (int, optional): Section 80D deductions. Defaults to 0.
        section_80gg (int, optional): Section 80GG deductions. Defaults to 0.
        section_80dd (int, optional): Section 80DD deductions. Defaults to 0.
        section_80ddb (int, optional): Section 80DDB deductions. Defaults to 0.
        section_24b (int, optional): Section 24(b) deductions. Defaults to 0.
        section_80ccd_1b (int, optional): Section 80CCD(1B) deductions. Defaults to 0.
        section_80ccd_2 (int, optional): Section 80CCD(2) deductions. Defaults to 0.
        section_80eea (int, optional): Section 80EEA deductions. Defaults to 0.
        section_80u (int, optional): Section 80U deductions. Defaults to 0.
        section_80eeb (int, optional): Section 80EEB deductions. Defaults to 0.
        section_80e (int, optional): Section 80E deductions. Defaults to 0.
        section_80g_50percent (int, optional): Section 80G 50% deductions. Defaults to 0.
        section_80g_100percent (int, optional): Section 80G 100% deductions. Defaults to 0.
        section_80gga (int, optional): Section 80GGA deductions. Defaults to 0.
        section_80ggc (int, optional): Section 80GGD deductions. Defaults to 0.
        rent_for_hra_exemption (int, optional): Rent paid for HRA exemption. Defaults to 0.
        professional_tax (int, optional): Professional tax. Defaults to 0.
        food_coupons (int, optional): Food coupons. Defaults to 0.
        other_exemption (int, optional): Other exemptions. Defaults to 0.
    """
    self.section_80c=min(section_80c,150000)
    self.section_80d=min(section_80d, 100000)
    self.section_80gg=section_80gg # calculated based on settings
    self.section_80dd=min(section_80dd, 1250000)
    self.section_80ddb=min(section_80ddb, 100000)
    self.section_24b=min(section_24b, 200000)
    self.section_80ccd_1b=min(section_80ccd_1b, 50000)
    self.section_80ccd_2=min(section_80ccd_2, 168001)
    self.section_80eea=min(section_80eea, 150000)
    self.section_80u=min(section_80u, 125000)
    self.section_80eeb=min(section_80eeb, 150000)
    self.section_80e=section_80e #no limit
    self.section_80g_50percent=section_80g_50percent #no limit
    self.section_80g_100percent=section_80g_100percent #no limit
    self.section_80gga=section_80gga #no limit
    self.section_80ggc=section_80ggc #no limit
    self._section_80tta = 0
    self._section_80ttb = 0
    self.rent_for_hra_exemption=rent_for_hra_exemption # calculated based on settings
    self.professional_tax=min(professional_tax, 2500)
    self.food_coupons=min(food_coupons, 26000)
    self.other_exemption=other_exemption #no limit

  
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
        + self.section_80ddb
        + self.section_24b
        + self.section_80ccd_1b
        + self.section_80ccd_2
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

