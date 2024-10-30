from django import forms

class BmiForm(forms.Form):
    height = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))