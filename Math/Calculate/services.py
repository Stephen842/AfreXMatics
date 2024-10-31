from django.core.cache import cache
import requests

# This function is to store all currency symbols and names in our cache memory for every 6 hours
def get_currency_choices():
    currency_choices = cache.get('currency_choices')
    
    if not currency_choices:
        currency_choices = fetch_currency_choices_from_api()
        cache.set('currency_choices', currency_choices, 21600) # 6 hours
    return currency_choices

# This function is to store the exchange rate of all currency to our cache memory within the interval of 6 hours
def get_exchange_rate(from_currency, to_currency):
    cache_key = f'exchange_rate_{from_currency}_{to_currency}'
    exchange_rate = cache.get(cache_key)

    if exchange_rate is  None:
        exchange_rate = fetch_exchange_rate_from_api(from_currency, to_currency)
        cache.set(cache_key, exchange_rate, 21600)
    return exchange_rate

# This function is to fetch list of all currency with their names and symbols using API call
def fetch_currency_choices_from_api():
    api_key = '7e62c2cbb19a937e8adf65b738254171'
    url = f'http://data.fixer.io/api/symbols?access_key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [(code, name) for code, name in data.get('symbols', {}).items()]
    except requests.RequestException as e:
        print(f'Error fetching currency choices: {e}')
        return []

# This function is to fetch the exchange rate between two currency using API call
def fetch_exchange_rate_from_api(from_currency, to_currency):
    api_key = '7e62c2cbb19a937e8adf65b738254171'
    url = f'http://data.fixer.io/api/latest?access_key={api_key}&symbols={from_currency},{to_currency}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = data.get('rates', {})

        #To calculate exchange rate between the two currencies
        exchange_rate = rates.get(to_currency) / rates.get(from_currency)
        return exchange_rate
    except requests.RequestException as e:
        print(f'Error fetching exchange rate: {e}')
        return None # (To return nothing if their is an error)
