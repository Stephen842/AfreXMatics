from django.shortcuts import render, redirect
from .forms import BmiForm, CurrencyConverterForm
from .services import get_currency_choices, get_exchange_rate
from decimal import Decimal


# Create your views here.

#This Function View is for the currency converter feature of this entire program
def currency_convert(request):
    result = None

    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            from_currency = form.cleaned_data['from_currency']
            to_currency = form.cleaned_data['to_currency']

            # Get the exchange rate using the caching function
            exchange_rate = get_exchange_rate(from_currency, to_currency)

            if exchange_rate is not None:
                # Ensure exchange_rate is Decimal
                exchange_rate = Decimal(exchange_rate)
                
                result = Decimal(amount) * exchange_rate # This is the calculated converted amount
            else:
                result = 'Error fetching exchange rate.'
    else:
        form = CurrencyConverterForm()

    context = {
        'form': form,
        'result': result,
        'currency_choices': get_currency_choices(),
        'title': 'QuickConvert: Real-Time Rates',
    }
        
    return render(request, 'pages/currency.html', context)

# This function is to calculate the Body Mass Index of a person
def calculate_bmi(request):
    bmi = None
    category = None

    if request.method == 'POST':
        form = BmiForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            bmi = weight / (height ** 2)
            bmi_str = f"{bmi:.2f}"  # Format BMI as a string with 2 decimal places

            # To calculate BMI category
            if bmi < 18.5:
                category = 'Underweight'
            elif 18.5 <=  bmi < 24.9:
                category = 'Normal weight'
            elif 25 <= bmi < 29.9:
                category = 'Overweight'
            else:
                category = 'Obesity'

            # Pass BMI data as URL paramters
            return redirect('bmi_result', bmi=bmi_str, category=category)

    else:
        form = BmiForm()

    context = {
        'form': form,
        'bmi': bmi,
        'category': category,
        'title': 'BMI Calculator: Know Your Numbers',
    }
    return render(request, 'pages/bmi.html', context)

# To display the result of the BMI calculations
def bmi_result(request, bmi, category):
    context = {
        'bmi': bmi,
        'category': category,
        'title': 'BMI Analysis: Your Health at a Glance',
    }
    return render(request, 'pages/bmi_result.html', context)
