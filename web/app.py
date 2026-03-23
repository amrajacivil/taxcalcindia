import os
import sys
from flask import Flask, render_template, request, jsonify

# Ensure the parent directory is in the path so we can import taxcalcindia
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from taxcalcindia.calculator import IncomeTaxCalculator
from taxcalcindia.models import (
    TaxSettings,
    SalaryIncome,
    BusinessIncome,
    CapitalGainsIncome,
    OtherIncome,
    Deductions,
    EmploymentType
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        
        # Extract and validate basic settings
        settings_data = data.get('settings', {})
        settings = TaxSettings(
            age=int(settings_data.get('age', 25)),
            financial_year=int(settings_data.get('financial_year', 2025)),
            is_metro_resident=settings_data.get('is_metro_resident', True),
            employment_type=EmploymentType(settings_data.get('employment_type', 'private'))
        )
        
        # Extract salary details
        salary_data = data.get('salary', {})
        salary = SalaryIncome(
            basic_and_da=float(salary_data.get('basic_and_da', 0)),
            hra=float(salary_data.get('hra', 0)),
            other_allowances=float(salary_data.get('other_allowances', 0)),
            bonus_and_commissions=float(salary_data.get('bonus_and_commissions', 0))
        )
        
        # Extract business and capital gains if provided (optional)
        business_data = data.get('business', {})
        business = BusinessIncome(
            business_income=float(business_data.get('business_income', 0)),
            property_income=float(business_data.get('property_income', 0))
        )
        
        cg_data = data.get('capital_gains', {})
        capital_gains = CapitalGainsIncome(
            short_term_at_normal=float(cg_data.get('short_term_at_normal', 0)),
            short_term_at_20_percent=float(cg_data.get('short_term_at_20_percent', 0)),
            long_term_at_12_5_percent=float(cg_data.get('long_term_at_12_5_percent', 0)),
            long_term_at_20_percent=float(cg_data.get('long_term_at_20_percent', 0))
        )
        
        other_income_data = data.get('other_income', {})
        other_income = OtherIncome(
            savings_account_interest=float(other_income_data.get('savings_account_interest', 0)),
            fixed_deposit_interest=float(other_income_data.get('fixed_deposit_interest', 0)),
            other_sources=float(other_income_data.get('other_sources', 0))
        )
        
        # Extract deductions
        deductions_data = data.get('deductions', {})
        deductions = Deductions(
            section_80c=float(deductions_data.get('section_80c', 0)),
            section_80d=float(deductions_data.get('section_80d', 0)),
            section_24b=float(deductions_data.get('section_24b', 0)),
            section_80ccd_1b=float(deductions_data.get('section_80ccd_1b', 0)),
            rent_for_hra_exemption=float(deductions_data.get('rent_for_hra_exemption', 0)),
            professional_tax=float(deductions_data.get('professional_tax', 0)),
            food_coupons=float(deductions_data.get('food_coupons', 0))
        )
        
        # Create calculator and calculate
        calc = IncomeTaxCalculator(
            settings=settings,
            salary=salary,
            business=business,
            capital_gains=capital_gains,
            other_income=other_income,
            deductions=deductions
        )
        
        result = calc.calculate_tax(is_comparision_needed=True, is_tax_per_slab_needed=True)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
