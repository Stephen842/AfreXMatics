from django import forms
from .services import get_currency_choices

#This Form is for the currency converter feature
class CurrencyConverterForm(forms.Form):
    amount = forms.DecimalField(required=True)
    from_currency = forms.ChoiceField(
            label='From Currency', choices=get_currency_choices(), required=True
    )
    to_currency = forms.ChoiceField(
            label='To Currency', choices=get_currency_choices(), required=True
    )

#This Form is for the BMI Feature
class BmiForm(forms.Form):
    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
