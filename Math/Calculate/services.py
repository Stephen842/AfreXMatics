from django.core.cache import cache
import requests
from django.utils.safestring import mark_safe

# This is a list of all present country code 
COUNTRY_CODES = {
    'AED': 'AE',  # United Arab Emirates Dirham
    'AFN': 'AF',  # Afghan Afghani
    'ALL': 'AL',  # Albanian Lek
    'AMD': 'AM',  # Armenian Dram
    'ANG': 'AN',  # Netherlands Antillean Guilder
    'AOA': 'AO',  # Angolan Kwanza
    'ARS': 'AR',  # Argentine Peso
    'AUD': 'AU',  # Australian Dollar
    'AWG': 'AW',  # Aruban Florin
    'AZN': 'AZ',  # Azerbaijani Manat
    'BAM': 'BA',  # Bosnia and Herzegovina Convertible Mark
    'BBD': 'BB',  # Barbadian Dollar
    'BDT': 'BD',  # Bangladeshi Taka
    'BGN': 'BG',  # Bulgarian Lev
    'BHD': 'BH',  # Bahraini Dinar
    'BIF': 'BI',  # Burundian Franc
    'BMD': 'BM',  # Bermudian Dollar
    'BND': 'BN',  # Brunei Dollar
    'BOB': 'BO',  # Bolivian Boliviano
    'BRL': 'BR',  # Brazilian Real
    'BSD': 'BS',  # Bahamian Dollar
    'BTN': 'BT',  # Bhutanese Ngultrum
    'BWP': 'BW',  # Botswana Pula
    'BYN': 'BY',  # Belarusian Ruble
    'BZD': 'BZ',  # Belize Dollar
    'CAD': 'CA',  # Canadian Dollar
    'CDF': 'CD',  # Congolese Franc
    'CHF': 'CH',  # Swiss Franc
    'CLP': 'CL',  # Chilean Peso
    'CNY': 'CN',  # Chinese Yuan
    'COP': 'CO',  # Colombian Peso
    'CRC': 'CR',  # Costa Rican Colón
    'CUP': 'CU',  # Cuban Peso
    'CVE': 'CV',  # Cape Verdean Escudo
    'CZK': 'CZ',  # Czech Koruna
    'DJF': 'DJ',  # Djiboutian Franc
    'DKK': 'DK',  # Danish Krone
    'DOP': 'DO',  # Dominican Peso
    'DZD': 'DZ',  # Algerian Dinar
    'EEK': 'EE',  # Estonian Kroon
    'EGP': 'EG',  # Egyptian Pound
    'ERN': 'ER',  # Eritrean Nakfa
    'ETB': 'ET',  # Ethiopian Birr
    'EUR': 'EU',  # Euro
    'FJD': 'FJ',  # Fijian Dollar
    'FKP': 'FK',  # Falkland Islands Pound
    'GBP': 'GB',  # British Pound Sterling
    'GEL': 'GE',  # Georgian Lari
    'GHS': 'GH',  # Ghanaian Cedi
    'GIP': 'GI',  # Gibraltar Pound
    'GMD': 'GM',  # Gambian Dalasi
    'GNF': 'GN',  # Guinean Franc
    'GTQ': 'GT',  # Guatemalan Quetzal
    'GYD': 'GY',  # Guyanese Dollar
    'HKD': 'HK',  # Hong Kong Dollar
    'HNL': 'HN',  # Honduran Lempira
    'HRK': 'HR',  # Croatian Kuna
    'HTG': 'HT',  # Haitian Gourde
    'HUF': 'HU',  # Hungarian Forint
    'IDR': 'ID',  # Indonesian Rupiah
    'ILS': 'IL',  # Israeli New Shekel
    'INR': 'IN',  # Indian Rupee
    'IQD': 'IQ',  # Iraqi Dinar
    'IRR': 'IR',  # Iranian Rial
    'ISK': 'IS',  # Icelandic Króna
    'JMD': 'JM',  # Jamaican Dollar
    'JPY': 'JP',  # Japanese Yen
    'KES': 'KE',  # Kenyan Shilling
    'KGS': 'KG',  # Kyrgyzstani Som
    'KHR': 'KH',  # Cambodian Riel
    'KPW': 'KP',  # North Korean Won
    'KRW': 'KR',  # South Korean Won
    'KWD': 'KW',  # Kuwaiti Dinar
    'KYD': 'KY',  # Cayman Islands Dollar
    'KZT': 'KZ',  # Kazakhstani Tenge
    'LAK': 'LA',  # Laotian Kip
    'LBP': 'LB',  # Lebanese Pound
    'LKR': 'LK',  # Sri Lankan Rupee
    'LRD': 'LR',  # Liberian Dollar
    'LSL': 'LS',  # Lesotho Loti
    'LYD': 'LY',  # Libyan Dinar
    'MAD': 'MA',  # Moroccan Dirham
    'MDL': 'MD',  # Moldovan Leu
    'MGA': 'MG',  # Malagasy Ariary
    'MKD': 'MK',  # Macedonian Denar
    'MMK': 'MM',  # Myanmar Kyat
    'MNT': 'MN',  # Mongolian Tögrög
    'MOP': 'MO',  # Macanese Pataca
    'MRU': 'MR',  # Mauritanian Ouguiya
    'MUR': 'MU',  # Mauritian Rupee
    'MVR': 'MV',  # Maldivian Rufiyaa
    'MWK': 'MW',  # Malawian Kwacha
    'MXN': 'MX',  # Mexican Peso
    'MYR': 'MY',  # Malaysian Ringgit
    'MZN': 'MZ',  # Mozambican Metical
    'NAD': 'NA',  # Namibian Dollar
    'NGN': 'NG',  # Nigerian Naira
    'NOK': 'NO',  # Norwegian Krone
    'NPR': 'NP',  # Nepalese Rupee
    'NZD': 'NZ',  # New Zealand Dollar
    'OMR': 'OM',  # Omani Rial
    'PAB': 'PA',  # Panamanian Balboa
    'PEN': 'PE',  # Peruvian Sol
    'PGK': 'PG',  # Papua New Guinean Kina
    'PHP': 'PH',  # Philippine Peso
    'PKR': 'PK',  # Pakistani Rupee
    'PLN': 'PL',  # Polish Zloty
    'PYG': 'PY',  # Paraguayan Guarani
    'QAR': 'QA',  # Qatari Rial
    'RON': 'RO',  # Romanian Leu
    'RSD': 'RS',  # Serbian Dinar
    'RUB': 'RU',  # Russian Ruble
    'RWF': 'RW',  # Rwandan Franc
    'SAR': 'SA',  # Saudi Riyal
    'SBD': 'SB',  # Solomon Islands Dollar
    'SCR': 'SC',  # Seychellois Rupee
    'SEK': 'SE',  # Swedish Krona
    'SGD': 'SG',  # Singapore Dollar
    'SHP': 'SH',  # Saint Helena Pound
    'SLL': 'SL',  # Sierra Leonean Leone
    'SOS': 'SO',  # Somali Shilling
    'SRD': 'SR',  # Surinamese Dollar
    'SSP': 'SS',  # South Sudanese Pound
    'STN': 'ST',  # São Tomé and Príncipe Dobra
    'SYP': 'SY',  # Syrian Pound
    'SZL': 'SZ',  # Swazi Lilangeni
    'THB': 'TH',  # Thai Baht
    'TJS': 'TJ',  # Tajikistani Somoni
    'TMT': 'TM',  # Turkmenistani Manat
    'TND': 'TN',  # Tunisian Dinar
    'TOP': 'TO',  # Tongan Paʻanga
    'TRY': 'TR',  # Turkish Lira
    'TTD': 'TT',  # Trinidad and Tobago Dollar
    'TWD': 'TW',  # New Taiwan Dollar
    'TZS': 'TZ',  # Tanzanian Shilling
    'UAH': 'UA',  # Ukrainian Hryvnia
    'UGX': 'UG',  # Ugandan Shilling
    'USD': 'US',  # United States Dollar
    'UYU': 'UY',  # Uruguayan Peso
    'UZS': 'UZ',  # Uzbekistani Som
}


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

    # Initialize an empty currency_choices list 
    currency_choices = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Create a list of tuples to contain the currency code, name and country code
        for code, name in data.get('symbols',{}).items():
            country_code = COUNTRY_CODES.get(code, None) # Get the country code if it exist
            currency_choices.append((code, name, country_code))

        return currency_choices
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
