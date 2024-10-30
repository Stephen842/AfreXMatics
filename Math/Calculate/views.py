from django.shortcuts import render, redirect
from .forms import BmiForm

# Create your views here.

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