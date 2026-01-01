
from models import SalaryIncome,BusinessIncome,OtherIncome,Deductions,TaxSettings
from slabs import get_tax_slabs


NEW_REGIME_KEY="new_regime"
OLD_REGIME_GEN_KEY="old_regime_general"
OLD_REGIME_SEN_KEY="old_regime_senior"
OLD_REGIME_SUPER_SEN_KEY="old_regime_super_senior"

class IncomeTaxCalculator:
    def __init__(
        self,settings: TaxSettings,
        salary: SalaryIncome | None = None,
        business: BusinessIncome | None = None,
        other_income: OtherIncome | None = None,
        deductions: Deductions | None = None
        ):
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
      return (
          self.salary.total
          + self.business.total
          + self.other_income.total
      )

    @property
    def taxable_income(self):
      return max(0, self.gross_income - self.settings.standard_deduction )

    def __calculate_tax_per_slab(self,taxable_income,slab):
      tax_per_slab={}
      tax=0
      previous_limit=0
      for limit,rate in slab:
        if self.taxable_income>previous_limit:
          taxable_part=min(limit-previous_limit,self.taxable_income-previous_limit)
          tax_for_current_slab = taxable_part * rate
          tax += tax_for_current_slab
          if limit == float("inf"):
            tax_per_slab[self.taxable_income-previous_limit]=tax_for_current_slab
          else:
            tax_per_slab[limit]=tax_for_current_slab
          previous_limit=limit

        else:
          break
      return tax,tax_per_slab


    def calculate_tax(self):
      slabs=get_tax_slabs(self.settings.financial_year,self.settings.age)

      new_regime_tax,new_regime_tax_per_slab=self.__calculate_tax_per_slab(self.taxable_income,slabs[NEW_REGIME_KEY])
      if self.settings.age>=60 and self.settings.age<80:
        old_regime_tax,old_regime_tax_per_slab=self.__calculate_tax_per_slab(self.taxable_income,slabs[OLD_REGIME_SEN_KEY])
      elif self.settings.age>=80:
        old_regime_tax,old_regime_tax_per_slab=self.__calculate_tax_per_slab(self.taxable_income,slabs[OLD_REGIME_SUPER_SEN_KEY])
      else:
        old_regime_tax,old_regime_tax_per_slab=self.__calculate_tax_per_slab(self.taxable_income,slabs[OLD_REGIME_GEN_KEY])
      old_regime_tax=max(old_regime_tax-self.deductions.total,0)

      if new_regime_tax>old_regime_tax:
        tax_difference=round(new_regime_tax-old_regime_tax)
        recommendation={
            "recommended_regime":"old",
            "summary":f"Old tax regime results in a savings of ₹ {tax_difference} compared to the new regime",
            "tax_savings_amount": tax_difference
        }
      else:
        tax_difference=round(old_regime_tax-new_regime_tax)
        recommendation={
            "recommended_regime":"new",
            "recommendation":f"New tax regime results in a savings of ₹{tax_difference} compared to the old regime",
            "tax_savings_amount": tax_difference
        }


      output_template={
          "income_summary":{
            "gross_income": self.gross_income,
            "gross_deductions":self.deductions.total,
            "taxable_income":self.taxable_income,
          },
          "tax_liability":{
              "new_regime":round(new_regime_tax,2),
              "old_regime":round(old_regime_tax,2),
          },
          "tax_per_slabs":{
              "new_regime":new_regime_tax_per_slab,
              "old_regime":old_regime_tax_per_slab
          },
          "tax_regime_comparison":recommendation
      }
      return output_template

