from django import forms
from .services import get_currency_choices
from django.utils.safestring import mark_safe

# This Form is the Calculator feature of this program
class CalculatorForm(forms.Form):
    # To accept general number input for many operations
    numbers = forms.CharField(
            label = 'Enter numbers (comma-seperated)',
            required = False,
    )

    # Choice of operation to select from so as to perform calculation
    operation = forms.ChoiceField(
            choices=[
                ('add', 'Addition'),
                ('subtract', 'Subtraction'),
                ('multiply', 'Multiplication'),
                ('divide', 'Division'),
                ('square', 'Square'),
                ('sqrt', 'Square Root'),
                ('root', 'Root'),
                ('exp', 'Exponentiation'),
                ('log', 'Logarithm'),
                ('sin', 'Sine'),
                ('cos', 'Cosine'),
                ('tan', 'Tangent'),
                ('hypotenuse', 'Calculate Hypotenuse'),
                ('adjacent', 'Calculate Adjacent'),
                ('opposite', 'Calculate Opposite'),
                ('diff', 'Differentiation'),
                ('int', 'Integration'),
                ('ode', 'Ordinary Differential Equation'),
                ('pde', 'Partial Differential Equation'),
                ('factorial', 'Factorial'),
                ('modulus', 'Modulus'),
                ('perm_comb', 'Permutation and Combination'),
                ('abs', 'Absolute Value'),
                ('arcsin', 'Arcsin'),
                ('arccos', 'Arccos'),
                ('arctan', 'Arctan'),
                ('hyperbolic', 'Hyperbolic Functions'),
                ('complex', 'Complex Numbers'),
                ('round', 'Rounding Functions'),
                ('log_base', 'Logarithm with Other Base'),
                ('SI', 'Simple Interest'),
                ('CI', 'Compound Interest'),
            ],
            label = 'Select Operation'
    )



#This Form is for the currency converter feature
class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'amount'  # Add the ID attribute here
        })
    )

    # Use the currency code as the value and display only the name
    currency_choices = get_currency_choices()

    from_currency = forms.ChoiceField(
        label='From Currency',
        choices=[
            (
                code, 
                mark_safe(f'<img src="https://flagcdn.com/{country_code.lower() if country_code else "default"}.svg" alt="{country_code or "default"}" /> {name} ({country_code or "N/A"})')
            ) 
            for code, name, country_code in currency_choices
        ], 
        required=True
    )

    to_currency = forms.ChoiceField(
        label='To Currency', 
        choices=[
            (
                code, 
                mark_safe(f'<img src="https://flagcdn.com/{country_code.lower() if country_code else "default"}.svg" alt="{country_code or "default"}" /> {name} ({country_code or "N/A"})')
            ) 
            for code, name, country_code in currency_choices
        ],
        required=True
    )

#This Form is for the BMI Feature
class BmiForm(forms.Form):
    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
