from django.core.cache import cache
import requests

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

# This is a list of all present country flags
COUNTRY_FLAGS = {
    'AED': 'https://flagcdn.com/ae.svg',  # United Arab Emirates Dirham
    'AFN': 'https://flagcdn.com/af.svg',  # Afghan Afghani
    'ALL': 'https://flagcdn.com/al.svg',  # Albanian Lek
    'AMD': 'https://flagcdn.com/am.svg',  # Armenian Dram
    'ANG': 'https://flagcdn.com/an.svg',  # Netherlands Antillean Guilder
    'AOA': 'https://flagcdn.com/ao.svg',  # Angolan Kwanza
    'ARS': 'https://flagcdn.com/ar.svg',  # Argentine Peso
    'AUD': 'https://flagcdn.com/au.svg',  # Australian Dollar
    'AWG': 'https://flagcdn.com/aw.svg',  # Aruban Florin
    'AZN': 'https://flagcdn.com/az.svg',  # Azerbaijani Manat
    'BAM': 'https://flagcdn.com/ba.svg',  # Bosnia and Herzegovina Convertible Mark
    'BBD': 'https://flagcdn.com/bb.svg',  # Barbadian Dollar
    'BDT': 'https://flagcdn.com/bd.svg',  # Bangladeshi Taka
    'BGN': 'https://flagcdn.com/bg.svg',  # Bulgarian Lev
    'BHD': 'https://flagcdn.com/bh.svg',  # Bahraini Dinar
    'BIF': 'https://flagcdn.com/bi.svg',  # Burundian Franc
    'BMD': 'https://flagcdn.com/bm.svg',  # Bermudian Dollar
    'BND': 'https://flagcdn.com/bn.svg',  # Brunei Dollar
    'BOB': 'https://flagcdn.com/bo.svg',  # Bolivian Boliviano
    'BRL': 'https://flagcdn.com/br.svg',  # Brazilian Real
    'BSD': 'https://flagcdn.com/bs.svg',  # Bahamian Dollar
    'BTN': 'https://flagcdn.com/bt.svg',  # Bhutanese Ngultrum
    'BWP': 'https://flagcdn.com/bw.svg',  # Botswana Pula
    'BYN': 'https://flagcdn.com/by.svg',  # Belarusian Ruble
    'BZD': 'https://flagcdn.com/bz.svg',  # Belize Dollar
    'CAD': 'https://flagcdn.com/ca.svg',  # Canadian Dollar
    'CDF': 'https://flagcdn.com/cd.svg',  # Congolese Franc
    'CHF': 'https://flagcdn.com/ch.svg',  # Swiss Franc
    'CLP': 'https://flagcdn.com/cl.svg',  # Chilean Peso
    'CNY': 'https://flagcdn.com/cn.svg',  # Chinese Yuan
    'COP': 'https://flagcdn.com/co.svg',  # Colombian Peso
    'CRC': 'https://flagcdn.com/cr.svg',  # Costa Rican Colón
    'CUP': 'https://flagcdn.com/cu.svg',  # Cuban Peso
    'CVE': 'https://flagcdn.com/cv.svg',  # Cape Verdean Escudo
    'CZK': 'https://flagcdn.com/cz.svg',  # Czech Koruna
    'DJF': 'https://flagcdn.com/dj.svg',  # Djiboutian Franc
    'DKK': 'https://flagcdn.com/dk.svg',  # Danish Krone
    'DOP': 'https://flagcdn.com/do.svg',  # Dominican Peso
    'DZD': 'https://flagcdn.com/dz.svg',  # Algerian Dinar
    'EEK': 'https://flagcdn.com/ee.svg',  # Estonian Kroon
    'EGP': 'https://flagcdn.com/eg.svg',  # Egyptian Pound
    'ERN': 'https://flagcdn.com/er.svg',  # Eritrean Nakfa
    'ETB': 'https://flagcdn.com/et.svg',  # Ethiopian Birr
    'EUR': 'https://flagcdn.com/eu.svg',  # Euro
    'FJD': 'https://flagcdn.com/fj.svg',  # Fijian Dollar
    'FKP': 'https://flagcdn.com/fk.svg',  # Falkland Islands Pound
    'GBP': 'https://flagcdn.com/gb.svg',  # British Pound Sterling
    'GEL': 'https://flagcdn.com/ge.svg',  # Georgian Lari
    'GHS': 'https://flagcdn.com/gh.svg',  # Ghanaian Cedi
    'GIP': 'https://flagcdn.com/gi.svg',  # Gibraltar Pound
    'GMD': 'https://flagcdn.com/gm.svg',  # Gambian Dalasi
    'GNF': 'https://flagcdn.com/gn.svg',  # Guinean Franc
    'GTQ': 'https://flagcdn.com/gt.svg',  # Guatemalan Quetzal
    'GYD': 'https://flagcdn.com/gy.svg',  # Guyanese Dollar
    'HKD': 'https://flagcdn.com/hk.svg',  # Hong Kong Dollar
    'HNL': 'https://flagcdn.com/hn.svg',  # Honduran Lempira
    'HRK': 'https://flagcdn.com/hr.svg',  # Croatian Kuna
    'HTG': 'https://flagcdn.com/ht.svg',  # Haitian Gourde
    'HUF': 'https://flagcdn.com/hu.svg',  # Hungarian Forint
    'IDR': 'https://flagcdn.com/id.svg',  # Indonesian Rupiah
    'ILS': 'https://flagcdn.com/il.svg',  # Israeli New Shekel
    'INR': 'https://flagcdn.com/in.svg',  # Indian Rupee
    'IQD': 'https://flagcdn.com/iq.svg',  # Iraqi Dinar
    'IRR': 'https://flagcdn.com/ir.svg',  # Iranian Rial
    'ISK': 'https://flagcdn.com/is.svg',  # Icelandic Króna
    'JMD': 'https://flagcdn.com/jm.svg',  # Jamaican Dollar
    'JPY': 'https://flagcdn.com/jp.svg',  # Japanese Yen
    'KES': 'https://flagcdn.com/ke.svg',  # Kenyan Shilling
    'KGS': 'https://flagcdn.com/kg.svg',  # Kyrgyzstani Som
    'KHR': 'https://flagcdn.com/kh.svg',  # Cambodian Riel
    'KPW': 'https://flagcdn.com/kp.svg',  # North Korean Won
    'KRW': 'https://flagcdn.com/kr.svg',  # South Korean Won
    'KWD': 'https://flagcdn.com/kw.svg',  # Kuwaiti Dinar
    'KYD': 'https://flagcdn.com/ky.svg',  # Cayman Islands Dollar
    'KZT': 'https://flagcdn.com/kz.svg',  # Kazakhstani Tenge
    'LAK': 'https://flagcdn.com/la.svg',  # Laotian Kip
    'LBP': 'https://flagcdn.com/lb.svg',  # Lebanese Pound
    'LKR': 'https://flagcdn.com/lk.svg',  # Sri Lankan Rupee
    'LRD': 'https://flagcdn.com/lr.svg',  # Liberian Dollar
    'LSL': 'https://flagcdn.com/ls.svg',  # Lesotho Loti
    'LYD': 'https://flagcdn.com/ly.svg',  # Libyan Dinar
    'MAD': 'https://flagcdn.com/ma.svg',  # Moroccan Dirham
    'MDL': 'https://flagcdn.com/md.svg',  # Moldovan Leu
    'MGA': 'https://flagcdn.com/mg.svg',  # Malagasy Ariary
    'MKD': 'https://flagcdn.com/mk.svg',  # Macedonian Denar
    'MMK': 'https://flagcdn.com/mm.svg',  # Myanmar Kyat
    'MNT': 'https://flagcdn.com/mn.svg',  # Mongolian Tögrög
    'MOP': 'https://flagcdn.com/mo.svg',  # Macanese Pataca
    'MRU': 'https://flagcdn.com/mr.svg',  # Mauritanian Ouguiya
    'MUR': 'https://flagcdn.com/mu.svg',  # Mauritian Rupee
    'MVR': 'https://flagcdn.com/mv.svg',  # Maldivian Rufiyaa
    'MWK': 'https://flagcdn.com/mw.svg',  # Malawian Kwacha
    'MXN': 'https://flagcdn.com/mx.svg',  # Mexican Peso
    'MYR': 'https://flagcdn.com/my.svg',  # Malaysian Ringgit
    'MZN': 'https://flagcdn.com/mz.svg',  # Mozambican Metical
    'NAD': 'https://flagcdn.com/na.svg',  # Namibian Dollar
    'NGN': 'https://flagcdn.com/ng.svg',  # Nigerian Naira
    'NIO': 'https://flagcdn.com/ni.svg',  # Nicaraguan Córdoba
    'NOK': 'https://flagcdn.com/no.svg',  # Norwegian Krone
    'NPR': 'https://flagcdn.com/np.svg',  # Nepalese Rupee
    'NZD': 'https://flagcdn.com/nz.svg',  # New Zealand Dollar
    'OMR': 'https://flagcdn.com/om.svg',  # Omani Rial
    'PAB': 'https://flagcdn.com/pa.svg',  # Panamanian Balboa
    'PEN': 'https://flagcdn.com/pe.svg',  # Peruvian Sol
    'PGK': 'https://flagcdn.com/pg.svg',  # Papua New Guinean Kina
    'PHP': 'https://flagcdn.com/ph.svg',  # Philippine Peso
    'PKR': 'https://flagcdn.com/pk.svg',  # Pakistani Rupee
    'PLN': 'https://flagcdn.com/pl.svg',  # Polish Zloty
    'PYG': 'https://flagcdn.com/py.svg',  # Paraguayan Guarani
    'QAR': 'https://flagcdn.com/qa.svg',  # Qatari Rial
    'RON': 'https://flagcdn.com/ro.svg',  # Romanian Leu
    'RSD': 'https://flagcdn.com/rs.svg',  # Serbian Dinar
    'RUB': 'https://flagcdn.com/ru.svg',  # Russian Ruble
    'RWF': 'https://flagcdn.com/rw.svg',  # Rwandan Franc
    'SAR': 'https://flagcdn.com/sa.svg',  # Saudi Riyal
    'SBD': 'https://flagcdn.com/sb.svg',  # Solomon Islands Dollar
    'SCR': 'https://flagcdn.com/sc.svg',  # Seychellois Rupee
    'SDG': 'https://flagcdn.com/sd.svg',  # Sudanese Pound
    'SEK': 'https://flagcdn.com/se.svg',  # Swedish Krona
    'SGD': 'https://flagcdn.com/sg.svg',  # Singapore Dollar
    'SHP': 'https://flagcdn.com/sh.svg',  # Saint Helena Pound
    'SLL': 'https://flagcdn.com/sl.svg',  # Sierra Leonean Leone
    'SOS': 'https://flagcdn.com/so.svg',  # Somali Shilling
    'SRD': 'https://flagcdn.com/sr.svg',  # Surinamese Dollar
    'SSP': 'https://flagcdn.com/ss.svg',  # South Sudanese Pound
    'STD': 'https://flagcdn.com/st.svg',  # São Tomé and Príncipe Dobra
    'SYP': 'https://flagcdn.com/sy.svg',  # Syrian Pound
    'SZL': 'https://flagcdn.com/sz.svg',  # Eswatini Lilangeni
    'THB': 'https://flagcdn.com/th.svg',  # Thai Baht
    'TJS': 'https://flagcdn.com/tj.svg',  # Tajikistani Somoni
    'TMT': 'https://flagcdn.com/tm.svg',  # Turkmenistani Manat
    'TND': 'https://flagcdn.com/tn.svg',  # Tunisian Dinar
    'TOP': 'https://flagcdn.com/to.svg',  # Tongan Paʻanga
    'TRY': 'https://flagcdn.com/tr.svg',  # Turkish Lira
    'TTD': 'https://flagcdn.com/tt.svg',  # Trinidad and Tobago Dollar
    'TWD': 'https://flagcdn.com/tw.svg',  # New Taiwan Dollar
    'TZS': 'https://flagcdn.com/tz.svg',  # Tanzanian Shilling
    'UAH': 'https://flagcdn.com/ua.svg',  # Ukrainian Hryvnia
    'UGX': 'https://flagcdn.com/ug.svg',  # Ugandan Shilling
    'USD': 'https://flagcdn.com/us.svg',  # United States Dollar
    'UYU': 'https://flagcdn.com/uy.svg',  # Uruguayan Peso
    'UZS': 'https://flagcdn.com/uz.svg',  # Uzbekistani Som
    'VES': 'https://flagcdn.com/ve.svg',  # Venezuelan Bolívar
    'VND': 'https://flagcdn.com/vn.svg',  # Vietnamese Dong
    'VUV': 'https://flagcdn.com/vu.svg',  # Vanuatu Vatu
    'WST': 'https://flagcdn.com/ws.svg',  # Samoan Tala
    'XAF': 'https://flagcdn.com/xaf.svg',  # Central African CFA Franc
    'XCD': 'https://flagcdn.com/xcd.svg',  # East Caribbean Dollar
    'XOF': 'https://flagcdn.com/xof.svg',  # West African CFA Franc
    'XPF': 'https://flagcdn.com/xpf.svg',  # CFP Franc
    'YER': 'https://flagcdn.com/ye.svg',  # Yemeni Rial
    'ZAR': 'https://flagcdn.com/za.svg',  # South African Rand
    'ZMW': 'https://flagcdn.com/zm.svg',  # Zambian Kwacha
    'ZWL': 'https://flagcdn.com/zw.svg',  # Zimbabwean Dollar
    'BTC': 'https://flagcdn.com/btc.svg'   # Bitcoin
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
            flag_url = COUNTRY_FLAGS.get(code, None)  # Get the flag URL
            currency_choices.append((code, name, country_code, flag_url))

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
