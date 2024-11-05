from django import forms
from .services import get_currency_choices
from django.utils.safestring import mark_safe

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
            choices=[(code, mark_safe(f"{flag_url} {name} ({country_code})")) for code, name, country_code, flag_url in currency_choices], 
            required=True
    )
    to_currency = forms.ChoiceField(
            label='To Currency', 
            choices=[(code, mark_safe(f"{flag_url} {name} ({country_code})")) for code, name, country_code, flag_url in currency_choices], 
            required=True
    )

#This Form is for the BMI Feature
class BmiForm(forms.Form):
    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
