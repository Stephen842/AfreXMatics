from django.shortcuts import render, redirect
import math
import cmath # For complex numbers
import sympy 
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

            try:
                # Parse number list if applicable
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
                    try: 
                        base_num = num_list[0]
                        power = num_list[1]
                        result = base_num ** power
                        explanation = f'{base_num} ^ {power} = {result}'
                    except IndexError:
                        error = 'Exponentiation require exactly two integers.'
                    except ValueError:
                        error = 'Invalid input. Please ensure you enter valid numbers.'

                # Below is for Square and Square root and the root of any number 
                elif operation == 'square':
                    result = num_list[0] ** 2
                    explanation = f'{num_list[0]} ^ 2 = {result}'

                elif operation == 'sqrt':
                    result = math.sqrt(num_list[0])
                    explanation = f'√{num_list[0]} = {result}'

                elif operation == 'root':
                    try:
                        number = num_list[0]
                        root_value = num_list[1] 

                        result = number ** (1 / root_value)
                        explanation = f'{root_value}√{number} = {result}'
                    except IndexError:
                        error = "Please provide two numbers separated by a comma (number, root_value)."
                    except ValueError:
                        error = "Invalid input. Please ensure you enter valid numbers."

                # Below is to run logarithmic calculations both for common and natural logarithms
                elif operation == 'log':
                    result = math.log(num_list[0])
                    explanation = f'ln({num_list[0]}) = {result}'
                
                elif operation == 'log_base':
                    try:
                        base_num = num_list[0]
                        value = num_list[1]
                        result = math.log(value, base_num)
                        explanation = f'log_{base_num} ({value}) = {result}'
                    except IndexError:
                        error = "Please provide two numbers separated by a comma (base number, value)."
                    except ValueError:
                        error = "Invalid input. Please ensure you enter valid numbers."

                # Below is to run trigonometric calculation which include Sine, Cosine and Tangent
                elif operation == 'sin':
                    angle = math.radians(num_list[0])
                    result = math.sin(angle)
                    explanation = f'sin({num_list[0]}) = {result}'

                elif operation == 'cos':
                    angle = math.radians(num_list[0])
                    result = math.cos(angle)
                    explanation = f'cos({num_list[0]}) = {result}'

                elif operation == 'tan':
                    angle = math.radians(num_list[0])
                    result = math.tan(angle)
                    explanation = f'tan({num_list[0]}) = {result}'

                # Below is to run Pythagorean Theorem by running calculations on the Hypotenuse, adjacent and opposite angle of a right angle triangle
                elif operation == 'hypotenuse':
                    try:
                        base = num_list[0]
                        height = num_list[1]
                        result = math.sqrt(base ** 2 + height ** 2)
                        explanation = f'√({base}^2 + {height}^2) = {result}'
                    except IndexError:
                        error = "Please enter two numbers separated by a comma for Pythagoras' theorem (base, height)."
                    except ValueError:
                        error = 'Invalid input. Please ensure you enter valid numbers.'
                
                elif operation == 'adjacent':
                    try:
                        hypotenuse = num_list[0]
                        height = num_list[1]
                        result = math.sqrt(hypotenuse ** 2 - height ** 2)
                        explanation = f'√({hypotenuse}^2 - {height}^2) = {result}'
                    except IndexError:
                        error = "Please enter two numbers separated by a comma for finding the adjacent side (hypotenuse, height)."
                    except ValueError:
                        error = 'Invalid input. Please ensure you enter valid numbers.'

                elif operation == 'opposite':
                    try:
                        hypotenuse = num_list[0]
                        base = num_list[1]
                        result = math.sqrt(hypotenuse ** 2 - base ** 2)
                        explanation = f'√({hypotenuse}^2 - {base}^2) = {result}'
                    except IndexError:
                        error = "Please enter two numbers separated by a comma for finding the opposite side (hypotenuse, base)."
                    except ValueError:
                        error = 'Invalid input. Please ensure you enter valid numbers.'

                # Below is to run Calculus calculations such as differentiation and integration
                elif operation == 'diff':
                    x = sympy.symbols('x')
                    expression = x ** 2
                    derivative = sympy.diff(expression, x)
                    result = derivative
                    explanation = f'd/dx of {expression} = {derivative}'

                elif operation == 'int':
                    x = sympy.symbols('x')
                    expression = x ** 2
                    integral = sympy.integrate(expression, x)
                    result = integral
                    explanation = f'∫({expression}) dx = {integral}'

                # Below is to run calculation on factorial
                elif operation == 'factorial':
                    if len(num_list) == 1 and num_list[0] >= 0:
                        result = math.factorial(int(num_list[0]))
                        explanation = f'{int(num_list[0])}! = {result}'
                    else:
                        error = 'Factorial requires a single non-negative integer.'
                
                # Below is to run modulus calculations
                elif operation == 'modulus':
                    if len(num_list) == 2:
                        result = num_list[0] % num_list[1]
                        explanation = f'{num_list[0]} % {num_list[1]} = {result}'
                    else:
                        error = 'Modulus requires two numbers.'
                
                # Below is to run calculations on permutation and commbination
                elif operation == 'perm_comb':
                    if len(num_list) == 2:
                        n, r = int(num_list[0]), int(num_list[1])
                        permutation = math.perm(n, r)
                        combination = math.comb(n, r)
                        result = {'Permutation': permutation, 'Combination': combination}
                        explanation = f'P({n}, {r}) = {permutation}, C({n}, {r}) = {combination}'
                    else:
                        error = 'Permutaion and Combination require exactly two integers.'
                
                # Below is to run calculations on absolute value
                elif operation == 'abs':
                    if len(num_list) == 1:
                        result = abs(num_list[0])
                        explanation = f'|{num_list[0]}| = {result}'
                    else:
                        error = 'Absolute value requires a single number.'

                # Below is to run calculations on inverse trigonometric functions
                elif operation == 'arcsin':
                    result = math.degrees(math.asin(num_list[0]))
                    explanation = f'arcsin({num_list[0]}) = {result}'

                elif operation == 'arccos':
                    result = math.degrees(math.acos(num_list[0]))
                    explanation = f'arccos({num_list[0]}) = {result}'

                elif operation == 'arctan':
                    result = math.degrees(math.atan(num_list[0]))
                    explanation = f'arctan({num_list[0]}) = {result}'

                # Below is to run calculation on Hyperbolic functions
                elif operation == 'hyperbolic':
                    sinh = math.sinh(num_list[0])
                    cosh = math.cosh(num_list[0])
                    tanh = math.tanh(num_list[0])
                    result = {'sinh': sinh, 'cosh': cosh, 'tanh': tanh,}
                    explanation = f'sinh({num_list[0]}) = {sinh}, cosh({num_list[0]}) = {cosh}, tanh({num_list[0]}) = {tanh}'

                # Below is run calculations on complex numbers
                elif operation == 'complex':
                    if len(num_list) == 2:
                        complex_num = complex(num_list[0, num_list[1]])
                        magnitude  = abs(complex_num)
                        phase = math.degrees(cmath.phase(complex_num))
                        result = {'Complex Number': complex_num, 'Magnitude': magnitude, 'Phase (degrees)': phase}
                        explanation = f'Complex: {complex_num}, Magnitude: |{complex_num}| = {magnitude}, Phase = {phase}°'
                    else:
                        error = 'Complex operation requires a real and an imaginary part.'

                # Below is for running calculations on rounding functions
                elif operation == 'round':
                    result = round(num_list[0])
                    explanation = f'Round ({num_list[0]}) = {result}'

                # Below is to run calculation on ordinary differential equation
                elif operation == 'ode':
                    x = sympy.symbols('x')
                    expression = x ** 2 - 4 * x + 3
                    solution = sympy.diff(expression, x, x) + sympy.diff(expression, x) + expression
                    result = solution
                    explanation = f'Solving ODE for {expression} gives solution: {solution}'

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
