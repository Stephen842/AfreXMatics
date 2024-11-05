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

# This is a list of all present country flags
COUNTRY_FLAGS = {
    'AED': mark_safe("<img src='https://flagcdn.com/ae.svg' alt='UAE flag' width='24' height='18'>"),  # United Arab Emirates Dirham
    'AFN': mark_safe("<img src='https://flagcdn.com/af.svg' alt='Afghan flag' width='24' height='18'>"),  # Afghan Afghani
    'ALL': mark_safe("<img src='https://flagcdn.com/al.svg' alt='Albanian flag' width='24' height='18'>"),  # Albanian Lek
    'AMD': mark_safe("<img src='https://flagcdn.com/am.svg' alt='Armenian flag' width='24' height='18'>"),  # Armenian Dram
    'ANG': mark_safe("<img src='https://flagcdn.com/an.svg' alt='Netherlands Antillean flag' width='24' height='18'>"),  # Netherlands Antillean Guilder
    'AOA': mark_safe("<img src='https://flagcdn.com/ao.svg' alt='Angolan flag' width='24' height='18'>"),  # Angolan Kwanza
    'ARS': mark_safe("<img src='https://flagcdn.com/ar.svg' alt='Argentine flag' width='24' height='18'>"),  # Argentine Peso
    'AUD': mark_safe("<img src='https://flagcdn.com/au.svg' alt='Australian flag' width='24' height='18'>"),  # Australian Dollar
    'AWG': mark_safe("<img src='https://flagcdn.com/aw.svg' alt='Aruban flag' width='24' height='18'>"),  # Aruban Florin
    'AZN': mark_safe("<img src='https://flagcdn.com/az.svg' alt='Azerbaijani flag' width='24' height='18'>"),  # Azerbaijani Manat
    'BAM': mark_safe("<img src='https://flagcdn.com/ba.svg' alt='Bosnia and Herzegovina flag' width='24' height='18'>"),  # Bosnia and Herzegovina Convertible Mark
    'BBD': mark_safe("<img src='https://flagcdn.com/bb.svg' alt='Barbadian flag' width='24' height='18'>"),  # Barbadian Dollar
    'BDT': mark_safe("<img src='https://flagcdn.com/bd.svg' alt='Bangladeshi flag' width='24' height='18'>"),  # Bangladeshi Taka
    'BGN': mark_safe("<img src='https://flagcdn.com/bg.svg' alt='Bulgarian flag' width='24' height='18'>"),  # Bulgarian Lev
    'BHD': mark_safe("<img src='https://flagcdn.com/bh.svg' alt='Bahraini flag' width='24' height='18'>"),  # Bahraini Dinar
    'BIF': mark_safe("<img src='https://flagcdn.com/bi.svg' alt='Burundian flag' width='24' height='18'>"),  # Burundian Franc
    'BMD': mark_safe("<img src='https://flagcdn.com/bm.svg' alt='Bermudian flag' width='24' height='18'>"),  # Bermudian Dollar
    'BND': mark_safe("<img src='https://flagcdn.com/bn.svg' alt='Bruneian flag' width='24' height='18'>"),  # Brunei Dollar
    'BOB': mark_safe("<img src='https://flagcdn.com/bo.svg' alt='Bolivian flag' width='24' height='18'>"),  # Bolivian Boliviano
    'BRL': mark_safe("<img src='https://flagcdn.com/br.svg' alt='Brazilian flag' width='24' height='18'>"),  # Brazilian Real
    'BSD': mark_safe("<img src='https://flagcdn.com/bs.svg' alt='Bahamian flag' width='24' height='18'>"),  # Bahamian Dollar
    'BTN': mark_safe("<img src='https://flagcdn.com/bt.svg' alt='Bhutanese flag' width='24' height='18'>"),  # Bhutanese Ngultrum
    'BWP': mark_safe("<img src='https://flagcdn.com/bw.svg' alt='Botswanan flag' width='24' height='18'>"),  # Botswana Pula
    'BYN': mark_safe("<img src='https://flagcdn.com/by.svg' alt='Belarusian flag' width='24' height='18'>"),  # Belarusian Ruble
    'BZD': mark_safe("<img src='https://flagcdn.com/bz.svg' alt='Belizean flag' width='24' height='18'>"),  # Belize Dollar
    'CAD': mark_safe("<img src='https://flagcdn.com/ca.svg' alt='Canadian flag' width='24' height='18'>"),  # Canadian Dollar
    'CDF': mark_safe("<img src='https://flagcdn.com/cd.svg' alt='Congolese flag' width='24' height='18'>"),  # Congolese Franc
    'CHF': mark_safe("<img src='https://flagcdn.com/ch.svg' alt='Swiss flag' width='24' height='18'>"),  # Swiss Franc
    'CLP': mark_safe("<img src='https://flagcdn.com/cl.svg' alt='Chilean flag' width='24' height='18'>"),  # Chilean Peso
    'CNY': mark_safe("<img src='https://flagcdn.com/cn.svg' alt='Chinese flag' width='24' height='18'>"),  # Chinese Yuan
    'COP': mark_safe("<img src='https://flagcdn.com/co.svg' alt='Colombian flag' width='24' height='18'>"),  # Colombian Peso
    'CRC': mark_safe("<img src='https://flagcdn.com/cr.svg' alt='Costa Rican flag' width='24' height='18'>"),  # Costa Rican Colón
    'CUP': mark_safe("<img src='https://flagcdn.com/cu.svg' alt='Cuban flag' width='24' height='18'>"),  # Cuban Peso
    'CVE': mark_safe("<img src='https://flagcdn.com/cv.svg' alt='Cape Verdean flag' width='24' height='18'>"),  # Cape Verdean Escudo
    'CZK': mark_safe("<img src='https://flagcdn.com/cz.svg' alt='Czech flag' width='24' height='18'>"),  # Czech Koruna
    'DJF': mark_safe("<img src='https://flagcdn.com/dj.svg' alt='Djiboutian flag' width='24' height='18'>"),  # Djiboutian Franc
    'DKK': mark_safe("<img src='https://flagcdn.com/dk.svg' alt='Danish flag' width='24' height='18'>"),  # Danish Krone
    'DOP': mark_safe("<img src='https://flagcdn.com/do.svg' alt='Dominican flag' width='24' height='18'>"),  # Dominican Peso
    'DZD': mark_safe("<img src='https://flagcdn.com/dz.svg' alt='Algerian flag' width='24' height='18'>"),  # Algerian Dinar
    'EEK': mark_safe("<img src='https://flagcdn.com/ee.svg' alt='Estonian flag' width='24' height='18'>"),  # Estonian Kroon
    'EGP': mark_safe("<img src='https://flagcdn.com/eg.svg' alt='Egyptian flag' width='24' height='18'>"),  # Egyptian Pound
    'ERN': mark_safe("<img src='https://flagcdn.com/er.svg' alt='Eritrean flag' width='24' height='18'>"),  # Eritrean Nakfa
    'ETB': mark_safe("<img src='https://flagcdn.com/et.svg' alt='Ethiopian flag' width='24' height='18'>"),  # Ethiopian Birr
    'EUR': mark_safe("<img src='https://flagcdn.com/eu.svg' alt='European flag' width='24' height='18'>"),  # Euro
    'FJD': mark_safe("<img src='https://flagcdn.com/fj.svg' alt='Fijian flag' width='24' height='18'>"),  # Fijian Dollar
    'FKP': mark_safe("<img src='https://flagcdn.com/fk.svg' alt='Falkland Islands flag' width='24' height='18'>"),  # Falkland Islands Pound
    'GBP': mark_safe("<img src='https://flagcdn.com/gb.svg' alt='British flag' width='24' height='18'>"),  # British Pound Sterling
    'GEL': mark_safe("<img src='https://flagcdn.com/ge.svg' alt='Georgian flag' width='24' height='18'>"),  # Georgian Lari
    'GHS': mark_safe("<img src='https://flagcdn.com/gh.svg' alt='Ghanaian flag' width='24' height='18'>"),  # Ghanaian Cedi
    'GIP': mark_safe("<img src='https://flagcdn.com/gi.svg' alt='Gibraltarian flag' width='24' height='18'>"),  # Gibraltar Pound
    'GMD': mark_safe("<img src='https://flagcdn.com/gm.svg' alt='Gambian flag' width='24' height='18'>"),  # Gambian Dalasi
    'GNF': mark_safe("<img src='https://flagcdn.com/gn.svg' alt='Guinean flag' width='24' height='18'>"),  # Guinean Franc
    'GTQ': mark_safe("<img src='https://flagcdn.com/gt.svg' alt='Guatemalan flag' width='24' height='18'>"),  # Guatemalan Quetzal
    'GYD': mark_safe("<img src='https://flagcdn.com/gy.svg' alt='Guyanese flag' width='24' height='18'>"),  # Guyanese Dollar
    'HKD': mark_safe("<img src='https://flagcdn.com/hk.svg' alt='Hong Kong flag' width='24' height='18'>"),  # Hong Kong Dollar
    'HNL': mark_safe("<img src='https://flagcdn.com/hn.svg' alt='Honduran flag' width='24' height='18'>"),  # Honduran Lempira
    'HRK': mark_safe("<img src='https://flagcdn.com/hr.svg' alt='Croatian flag' width='24' height='18'>"),  # Croatian Kuna
    'HTG': mark_safe("<img src='https://flagcdn.com/ht.svg' alt='Haitian flag' width='24' height='18'>"),  # Haitian Gourde
    'HUF': mark_safe("<img src='https://flagcdn.com/hu.svg' alt='Hungarian flag' width='24' height='18'>"),  # Hungarian Forint
    'IDR': mark_safe("<img src='https://flagcdn.com/id.svg' alt='Indonesian flag' width='24' height='18'>"),  # Indonesian Rupiah
    'ILS': mark_safe("<img src='https://flagcdn.com/il.svg' alt='Israeli flag' width='24' height='18'>"),  # Israeli New Shekel
    'INR': mark_safe("<img src='https://flagcdn.com/in.svg' alt='Indian flag' width='24' height='18'>"),  # Indian Rupee
    'IQD': mark_safe("<img src='https://flagcdn.com/iq.svg' alt='Iraqi flag' width='24' height='18'>"),  # Iraqi Dinar
    'IRR': mark_safe("<img src='https://flagcdn.com/ir.svg' alt='Iranian flag' width='24' height='18'>"),  # Iranian Rial
    'ISK': mark_safe("<img src='https://flagcdn.com/is.svg' alt='Icelandic flag' width='24' height='18'>"),  # Icelandic Króna
    'JMD': mark_safe("<img src='https://flagcdn.com/jm.svg' alt='Jamaican flag' width='24' height='18'>"),  # Jamaican Dollar
    'JOD': mark_safe("<img src='https://flagcdn.com/jo.svg' alt='Jordanian flag' width='24' height='18'>"),  # Jordanian Dinar
    'JPY': mark_safe("<img src='https://flagcdn.com/jp.svg' alt='Japanese flag' width='24' height='18'>"),  # Japanese Yen
    'KES': mark_safe("<img src='https://flagcdn.com/ke.svg' alt='Kenyan flag' width='24' height='18'>"),  # Kenyan Shilling
    'KGS': mark_safe("<img src='https://flagcdn.com/kg.svg' alt='Kyrgyz flag' width='24' height='18'>"),  # Kyrgyzstani Som
    'KHR': mark_safe("<img src='https://flagcdn.com/kh.svg' alt='Cambodian flag' width='24' height='18'>"),  # Cambodian Riel
    'KMF': mark_safe("<img src='https://flagcdn.com/km.svg' alt='Comorian flag' width='24' height='18'>"),  # Comorian Franc
    'KPW': mark_safe("<img src='https://flagcdn.com/kp.svg' alt='North Korean flag' width='24' height='18'>"),  # North Korean Won
    'KRW': mark_safe("<img src='https://flagcdn.com/kr.svg' alt='South Korean flag' width='24' height='18'>"),  # South Korean Won
    'KWD': mark_safe("<img src='https://flagcdn.com/kw.svg' alt='Kuwaiti flag' width='24' height='18'>"),  # Kuwaiti Dinar
    'KYD': mark_safe("<img src='https://flagcdn.com/ky.svg' alt='Cayman Islands flag' width='24' height='18'>"),  # Cayman Islands Dollar
    'KZT': mark_safe("<img src='https://flagcdn.com/kz.svg' alt='Kazakh flag' width='24' height='18'>"),  # Kazakhstani Tenge
    'LAK': mark_safe("<img src='https://flagcdn.com/la.svg' alt='Laotian flag' width='24' height='18'>"),  # Laotian Kip
    'LBP': mark_safe("<img src='https://flagcdn.com/lb.svg' alt='Lebanese flag' width='24' height='18'>"),  # Lebanese Pound
    'LKR': mark_safe("<img src='https://flagcdn.com/lk.svg' alt='Sri Lankan flag' width='24' height='18'>"),  # Sri Lankan Rupee
    'LRD': mark_safe("<img src='https://flagcdn.com/lr.svg' alt='Liberian flag' width='24' height='18'>"),  # Liberian Dollar
    'LSL': mark_safe("<img src='https://flagcdn.com/ls.svg' alt='Lesotho flag' width='24' height='18'>"),  # Lesotho Loti
    'LTL': mark_safe("<img src='https://flagcdn.com/lt.svg' alt='Lithuanian flag' width='24' height='18'>"),  # Lithuanian Litas
    'LYD': mark_safe("<img src='https://flagcdn.com/ly.svg' alt='Libyan flag' width='24' height='18'>"),  # Libyan Dinar
    'MAD': mark_safe("<img src='https://flagcdn.com/ma.svg' alt='Moroccan flag' width='24' height='18'>"),  # Moroccan Dirham
    'MDL': mark_safe("<img src='https://flagcdn.com/md.svg' alt='Moldovan flag' width='24' height='18'>"),  # Moldovan Leu
    'MGA': mark_safe("<img src='https://flagcdn.com/mg.svg' alt='Malagasy flag' width='24' height='18'>"),  # Malagasy Ariary
    'MKD': mark_safe("<img src='https://flagcdn.com/mk.svg' alt='Macedonian flag' width='24' height='18'>"),  # Macedonian Denar
    'MMK': mark_safe("<img src='https://flagcdn.com/mm.svg' alt='Burmese flag' width='24' height='18'>"),  # Myanmar Kyat
    'MNT': mark_safe("<img src='https://flagcdn.com/mn.svg' alt='Mongolian flag' width='24' height='18'>"),  # Mongolian Tögrög
    'MOP': mark_safe("<img src='https://flagcdn.com/mo.svg' alt='Macao flag' width='24' height='18'>"),  # Macanese Pataca
    'MRU': mark_safe("<img src='https://flagcdn.com/mr.svg' alt='Mauritanian flag' width='24' height='18'>"),  # Mauritanian Ouguiya
    'MUR': mark_safe("<img src='https://flagcdn.com/mu.svg' alt='Mauritian flag' width='24' height='18'>"),  # Mauritian Rupee
    'MVR': mark_safe("<img src='https://flagcdn.com/mv.svg' alt='Maldivian flag' width='24' height='18'>"),  # Maldivian Rufiyaa
    'MWK': mark_safe("<img src='https://flagcdn.com/mw.svg' alt='Malawian flag' width='24' height='18'>"),  # Malawian Kwacha
    'MXN': mark_safe("<img src='https://flagcdn.com/mx.svg' alt='Mexican flag' width='24' height='18'>"),  # Mexican Peso
    'MYR': mark_safe("<img src='https://flagcdn.com/my.svg' alt='Malaysian flag' width='24' height='18'>"),  # Malaysian Ringgit
    'MZN': mark_safe("<img src='https://flagcdn.com/mz.svg' alt='Mozambican flag' width='24' height='18'>"),  # Mozambican Metical
    'NAD': mark_safe("<img src='https://flagcdn.com/na.svg' alt='Namibian flag' width='24' height='18'>"),  # Namibian Dollar
    'NGN': mark_safe("<img src='https://flagcdn.com/ng.svg' alt='Nigerian flag' width='24' height='18'>"),  # Nigerian Naira
    'NIO': mark_safe("<img src='https://flagcdn.com/ni.svg' alt='Nicaraguan flag' width='24' height='18'>"),  # Nicaraguan Córdoba
    'NOK': mark_safe("<img src='https://flagcdn.com/no.svg' alt='Norwegian flag' width='24' height='18'>"),  # Norwegian Krone
    'NPR': mark_safe("<img src='https://flagcdn.com/np.svg' alt='Nepalese flag' width='24' height='18'>"),  # Nepalese Rupee
    'NZD': mark_safe("<img src='https://flagcdn.com/nz.svg' alt='New Zealand flag' width='24' height='18'>"),  # New Zealand Dollar
    'PAB': mark_safe("<img src='https://flagcdn.com/pa.svg' alt='Panamanian flag' width='24' height='18'>"),  # Panamanian Balboa
    'PEN': mark_safe("<img src='https://flagcdn.com/pe.svg' alt='Peruvian flag' width='24' height='18'>"),  # Peruvian Sol
    'PGK': mark_safe("<img src='https://flagcdn.com/pg.svg' alt='Papua New Guinean flag' width='24' height='18'>"),  # Papua New Guinean Kina
    'PHP': mark_safe("<img src='https://flagcdn.com/ph.svg' alt='Philippine flag' width='24' height='18'>"),  # Philippine Peso
    'PKR': mark_safe("<img src='https://flagcdn.com/pk.svg' alt='Pakistani flag' width='24' height='18'>"),  # Pakistani Rupee
    'PLN': mark_safe("<img src='https://flagcdn.com/pl.svg' alt='Polish flag' width='24' height='18'>"),  # Polish Zloty
    'PYG': mark_safe("<img src='https://flagcdn.com/py.svg' alt='Paraguayan flag' width='24' height='18'>"),  # Paraguayan Guarani
    'QAR': mark_safe("<img src='https://flagcdn.com/qa.svg' alt='Qatari flag' width='24' height='18'>"),  # Qatari Rial
    'RON': mark_safe("<img src='https://flagcdn.com/ro.svg' alt='Romanian flag' width='24' height='18'>"),  # Romanian Leu
    'RSD': mark_safe("<img src='https://flagcdn.com/rs.svg' alt='Serbian flag' width='24' height='18'>"),  # Serbian Dinar
    'RUB': mark_safe("<img src='https://flagcdn.com/ru.svg' alt='Russian flag' width='24' height='18'>"),  # Russian Ruble
    'RWF': mark_safe("<img src='https://flagcdn.com/rw.svg' alt='Rwandan flag' width='24' height='18'>"),  # Rwandan Franc
    'SAR': mark_safe("<img src='https://flagcdn.com/sa.svg' alt='Saudi Arabian flag' width='24' height='18'>"),  # Saudi Riyal
    'SBD': mark_safe("<img src='https://flagcdn.com/sb.svg' alt='Solomon Islands flag' width='24' height='18'>"),  # Solomon Islands Dollar
    'SCR': mark_safe("<img src='https://flagcdn.com/sc.svg' alt='Seychellois flag' width='24' height='18'>"),  # Seychellois Rupee
    'SDG': mark_safe("<img src='https://flagcdn.com/sd.svg' alt='Sudanese flag' width='24' height='18'>"),  # Sudanese Pound
    'SEK': mark_safe("<img src='https://flagcdn.com/se.svg' alt='Swedish flag' width='24' height='18'>"),  # Swedish Krona
    'SGD': mark_safe("<img src='https://flagcdn.com/sg.svg' alt='Singaporean flag' width='24' height='18'>"),  # Singapore Dollar
    'SHP': mark_safe("<img src='https://flagcdn.com/sh.svg' alt='Saint Helena flag' width='24' height='18'>"),  # Saint Helena Pound
    'SLL': mark_safe("<img src='https://flagcdn.com/sl.svg' alt='Sierra Leonean flag' width='24' height='18'>"),  # Sierra Leonean Leone
    'SOS': mark_safe("<img src='https://flagcdn.com/so.svg' alt='Somali flag' width='24' height='18'>"),  # Somali Shilling
    'SRD': mark_safe("<img src='https://flagcdn.com/sr.svg' alt='Surinamese flag' width='24' height='18'>"),  # Surinamese Dollar
    'SZL': mark_safe("<img src='https://flagcdn.com/sz.svg' alt='Swazi flag' width='24' height='18'>"),  # Swazi Lilangeni
    'THB': mark_safe("<img src='https://flagcdn.com/th.svg' alt='Thai flag' width='24' height='18'>"),  # Thai Baht
    'TJS': mark_safe("<img src='https://flagcdn.com/tj.svg' alt='Tajik flag' width='24' height='18'>"),  # Tajikistani Somoni
    'TMT': mark_safe("<img src='https://flagcdn.com/tm.svg' alt='Turkmen flag' width='24' height='18'>"),  # Turkmenistani Manat
    'TND': mark_safe("<img src='https://flagcdn.com/tn.svg' alt='Tunisian flag' width='24' height='18'>"),  # Tunisian Dinar
    'TOP': mark_safe("<img src='https://flagcdn.com/to.svg' alt='Tongan flag' width='24' height='18'>"),  # Tongan Paʻanga
    'TRY': mark_safe("<img src='https://flagcdn.com/tr.svg' alt='Turkish flag' width='24' height='18'>"),  # Turkish Lira
    'TTD': mark_safe("<img src='https://flagcdn.com/tt.svg' alt='Trinidad and Tobago flag' width='24' height='18'>"),  # Trinidad and Tobago Dollar
    'TWD': mark_safe("<img src='https://flagcdn.com/tw.svg' alt='Taiwan flag' width='24' height='18'>"),  # New Taiwan Dollar
    'TZS': mark_safe("<img src='https://flagcdn.com/tz.svg' alt='Tanzanian flag' width='24' height='18'>"),  # Tanzanian Shilling
    'UAH': mark_safe("<img src='https://flagcdn.com/ua.svg' alt='Ukrainian flag' width='24' height='18'>"),  # Ukrainian Hryvnia
    'UGX': mark_safe("<img src='https://flagcdn.com/ug.svg' alt='Ugandan flag' width='24' height='18'>"),  # Ugandan Shilling
    'USD': mark_safe("<img src='https://flagcdn.com/us.svg' alt='United States flag' width='24' height='18'>"),  # United States Dollar
    'UYU': mark_safe("<img src='https://flagcdn.com/uy.svg' alt='Uruguayan flag' width='24' height='18'>"),  # Uruguayan Peso
    'UZS': mark_safe("<img src='https://flagcdn.com/uz.svg' alt='Uzbekistani flag' width='24' height='18'>"),  # Uzbekistani Som
    'VES': mark_safe("<img src='https://flagcdn.com/ve.svg' alt='Venezuelan flag' width='24' height='18'>"),  # Venezuelan Bolívar
    'VND': mark_safe("<img src='https://flagcdn.com/vn.svg' alt='Vietnamese flag' width='24' height='18'>"),  # Vietnamese Dong
    'VUV': mark_safe("<img src='https://flagcdn.com/vu.svg' alt='Vanuatuan flag' width='24' height='18'>"),  # Vanuatu Vatu
    'WST': mark_safe("<img src='https://flagcdn.com/ws.svg' alt='Samoan flag' width='24' height='18'>"),  # Samoan Tala
    'XAF': mark_safe("<img src='https://flagcdn.com/xaf.svg' alt='Central African CFA franc' width='24' height='18'>"),  # Central African CFA Franc
    'XCD': mark_safe("<img src='https://flagcdn.com/xcd.svg' alt='East Caribbean Dollar' width='24' height='18'>"),  # East Caribbean Dollar
    'XOF': mark_safe("<img src='https://flagcdn.com/xof.svg' alt='West African CFA franc' width='24' height='18'>"),  # West African CFA Franc
    'XPF': mark_safe("<img src='https://flagcdn.com/xpf.svg' alt='CFP Franc' width='24' height='18'>"),  # CFP Franc
    'ZAR': mark_safe("<img src='https://flagcdn.com/za.svg' alt='South African flag' width='24' height='18'>"),  # South African Rand
    'ZMW': mark_safe("<img src='https://flagcdn.com/zm.svg' alt='Zambian flag' width='24' height='18'>"),  # Zambian Kwacha
    'ZWL': mark_safe("<img src='https://flagcdn.com/zw.svg' alt='Zimbabwean flag' width='24' height='18'>"),  # Zimbabwean Dollar
    'BTC': mark_safe("<img src='https://flagcdn.com/btc.svg' alt='bitcoin logo' width='24' height='18'>")   # Bitcoin
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
            currency_choices.append((code, name, country_code, mark_safe(flag_url)))

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
