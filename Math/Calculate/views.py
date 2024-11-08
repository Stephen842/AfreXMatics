from django.shortcuts import render, redirect
import math
import cmath # For complex numbers
from sympy import symbols, diff, integrate
from .forms import CalculatorForm
from .forms import BmiForm, CurrencyConverterForm
from .services import get_currency_choices, get_exchange_rate
from decimal import Decimal


# Create your views here.

# This function below is for all mathematical calculations this program will be running calculations of
def calculate(request):
    result = None
    explanation = None
    error = None

    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            # Retrieve data from form
            operation = form.cleaned_data.get('operation')
            numbers = form.cleaned_data.get('numbers')
            angle = form.cleaned_data.get('angle')
            base = form.cleaned_data.get('base')
            height = form.cleaned_data.get('height')
            side_a = form.cleaned_data.get('side_a')
            side_b = form.cleaned_data.get('side_b')

            try:
                #Parse number list if applicable
                num_list = [float(n) for n in numbers.split(',')] if numbers else []

                # Below covers basic arithmetic operations
                if operation == 'add':
                    result = sum(num_list)
                    explanation = ' + '.join(str(n) for n in num_list) + f' = {result}'

                elif operation == 'subtract':
                    result = num_list[0]
                    explanation = str(num_list[0])
                    for n in num_list[1:]:
                        result -= n
                        explanation += f' - {n}'
                    explanation += f' = {result}'

                elif operation == 'multiply':
                    result = math.prod(num_list)
                    explanation = ' * '.join(str(n) for n in num_list) + f' = {result}'

                elif operation == 'divide':
                    result = num_list[0]
                    explanation = str(num_list[0])
                    for n in num_list[1:]:
                        if n == 0:
                            error = 'Cannot divide by zero.'
                            break
                        result /= n
                        explanation += f' / {n}'
                    explanation += f' = {result}'

                # Below is to run calculation on exponentiation and indices
                elif operation == 'exp':
                    base_num = num_list[0]
                    power = num_list[1]
                    result = base_num ** power
                    explanation = f'{base_num} ^ {power} = {result}'

                # Below is for Square and Square root
                elif operation == 'square':
                    result = num_list ** 2
                    explanation = f'{num_list[0]} ^ 2 = {result}'

                elif operation == 'sqrt':
                    result = math.sqrt(num_list[0])
                    explanation = f'√{num_list[0]} = {result}'

                # Below is for the logarithms both for common and natural log
                elif operation == 'log':
                    result = math.log(num_list[0])
                    explanation = f'ln({num_list[0]}) = {result}'
                
                elif operation == 'log_base':
                    base_num = num_list[0]
                    value = num_list[1]
                    result = math.log(value, base_num)
                    explanation = f'log_{base_num} ({value}) = {result}'

                # Below is to run trigonometric calculation which include Sine, Cosine and Tangent
                elif operation == 'sin':
                    result = math.sin(math.radians(angle))
                    explanation = f'sin({angle}) = {result}'

                elif operation == 'cos':
                    result = math.cos(math.radians(angle))
                    explanation = f'cos({angle}) = {result}'

                elif operation == 'tan':
                    result = math.tan(math.radians(angle))
                    explanation = f'tan({angle}) = {result}'

                # Below is to run Pythagoras and Hypotenuse calculations
                elif operation == 'pythagoras':
                    if not (base and height):
                        error = "Both base and height are required for Pythagoras' theorem."
                    else:
                        result = math.sqrt(base ** 2 + height ** 2)
                        explanation = f'√({base} ^ 2 + {height} ^ 2) = {result}'
                
                elif operation == 'hypotenuse':
                    result = math.sqrt(side_a ** 2 + side_b ** 2)
                    explanation = f'√({side_a} ^ 2 + {side_b} ^ 2)'

                # Below is to run Calculus calculations such as differentiation and integration
                elif operation == 'diff':
                    x = symbols('x')
                    expression = x ** 2
                    derivative = diff(expression, x)
                    result = derivative
                    explanation = f'd/dx of {expression} = {derivative}'

                elif operation == 'int':
                    x = symbols('x')
                    expression = x ** 2
                    integral = integrate(expression, x)
                    result = integral
                    explanation = f'∫({expression}) dx = {integral}'
            except ValueError:
                error = 'Please ensure all input are valid numbers.'
            except Exception as e:
                error = str(e)
        else:
            error = 'Form data is invalid.'
    else:
        form = CalculatorForm()

    context={
        'title': '',
        'form': form,
        'result': result,
        'explanation': explanation,
        'error': error,
    }
    return render(request, 'pages/calculate.html', context)

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
