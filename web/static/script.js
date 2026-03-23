document.getElementById('taxForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = {
        settings: {
            age: formData.get('age'),
            financial_year: formData.get('financial_year'),
            employment_type: formData.get('employment_type'),
            is_metro_resident: e.target.is_metro_resident.checked
        },
        salary: {
            basic_and_da: formData.get('basic_and_da'),
            hra: formData.get('hra'),
            other_allowances: formData.get('other_allowances'),
            bonus_and_commissions: formData.get('bonus')
        },
        deductions: {
            rent_for_hra_exemption: formData.get('rent_paid'),
            section_80c: formData.get('section_80c'),
            section_80d: formData.get('section_80d'),
            professional_tax: formData.get('professional_tax')
        }
    };

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.error) {
            alert('Error: ' + result.error);
            return;
        }

        updateUI(result);
    } catch (err) {
        console.error('Failed to calculate:', err);
        alert('An unexpected error occurred.');
    }
});

function updateUI(result) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';

    const comp = result.tax_regime_comparison;
    const newReg = result.tax_liability.new_regime;
    const oldReg = result.tax_liability.old_regime;
    const inc = result.income_summary;

    // Recommendation
    document.getElementById('recommendedText').innerText = 
        (comp.recommended_regime === 'new' ? 'New Regime' : 'Old Regime') + ' is better!';
    document.getElementById('savingsText').innerText = 
        `You save ₹${comp.tax_savings_amount.toLocaleString('en-IN')} annually.`;

    // New Regime Details
    document.getElementById('newTotalTax').innerText = `₹${newReg.total.toLocaleString('en-IN')}`;
    document.getElementById('newTaxableIncome').innerText = `₹${inc.new_regime_taxable_income.toLocaleString('en-IN')}`;
    document.getElementById('newBaseTax').innerText = `₹${newReg.components.initial_tax.toLocaleString('en-IN')}`;
    document.getElementById('newCess').innerText = `₹${newReg.components.cess.toLocaleString('en-IN')}`;

    // Old Regime Details
    document.getElementById('oldTotalTax').innerText = `₹${oldReg.total.toLocaleString('en-IN')}`;
    document.getElementById('oldTaxableIncome').innerText = `₹${inc.old_regime_taxable_income.toLocaleString('en-IN')}`;
    document.getElementById('oldBaseTax').innerText = `₹${oldReg.components.initial_tax.toLocaleString('en-IN')}`;
    document.getElementById('oldCess').innerText = `₹${oldReg.components.cess.toLocaleString('en-IN')}`;

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}
