import time
from itertools import product
import pandas as pd
from os import path
import requests

RAPID_API_KEY = '7a3621970amsh9275d1c7c9ed661p15c96ajsnbc45c95d106c'
country_code = 'DE'
origin_id = 'MUC-sky'
destination_id = 'HNL'
trip_duration_in_dys=10
outbound_date = '2021-01-30'
inboundDate = (datetime.strptime(outbound_date, '%Y-%m-%d') + timedelta(days=trip_duration_in_dys)).strftime('%Y-%m-%d')


def get_prices_for(origin, destination, departure_date, return_date, country):
    if not RAPID_API_KEY:
        raise ValueError('''RAPID_API_KEY is empty.
        Please get your API KEY at https://rapidapi.com/ and set RAPID_API_KEY = 'API KEY'.
        ''')

    session_id = _init_query_session(origin, destination, departure_date, return_date, country)
    for (price, link) in _get_session_offers(session_id):
        yield {
            'origin': origin,
            'destination': destination,
            'departure_date': departure_date,
            'return_date': return_date,
            'country': country,
            'price': price,
            'link': link
        }


def _init_query_session(origin, destination, departure_date, return_date, country):
    print(f'Searching offers for {origin} -> {destination} ({country}, {departure_date} - {return_date})')
    response = _request('pricing/v1.0', method='post', data={
        'outboundDate': departure_date,
        'inboundDate': return_date,
        'country': country,
        'originPlace': origin,
        'destinationPlace': destination,
        'cabinClass': 'economy',
        'adults': 1,
        'children': 0,
        'infants': 0,
        'currency': 'USD',
        'locale': 'en-US',
    })

    if not response.ok:
        raise Exception('Got an exception while creating a new session ' + response.text)
    
    session_id = path.basename(response.headers['Location'])
    print(f'Session {session_id} succesfully created.')
    return session_id


def _get_session_offers(session_id):
    print(f'Fetching session {session_id} offers.')
    while True:
        time.sleep(1)
        response = _request(f'pricing/uk2/v1.0/{session_id}?pageIndex=0&pageSize=100', method='get')
        data = response.json()
        if data['Status'].lower() == 'updatescomplete':
            break

    print(f'Parsing session {session_id} offers.')
    for itinerary in data['Itineraries']:
        for pricing in itinerary['PricingOptions']:
            yield (pricing['Price'], pricing['DeeplinkUrl'])


def _request(url_path, method, data=None):
    url = f'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/{url_path}'
    if method.lower() == 'get':
        return requests.get(url, 
            headers={
                'X-RapidAPI-Host': 'skyscanner-skyscanner-flight-search-v1.p.rapidapi.com',
                'X-RapidAPI-Key': RAPID_API_KEY
            })
    else:
        return requests.post(url,
            data=data,
            headers={
                'X-RapidAPI-Host': 'skyscanner-skyscanner-flight-search-v1.p.rapidapi.com',
                'X-RapidAPI-Key': RAPID_API_KEY,
                'Content-Type': 'application/x-www-form-urlencoded'
            })

df = pd.DataFrame(columns=['origin', 'destination', 'departure_date', 'return_date', 'price', 'country', 'link'])

try:
    time.sleep(1)
    offers = list(get_prices_for(
        origin_id,
        destination_id,
        outbound_date,
        inboundDate,
        country_code
    ))
    df = df.append(offers)
except Exception as e:
    print(f'EXCEPTION while processing')
    time.sleep(2)



https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US/USD/en-US/SFO-sky/JFK-sky/2019-09-01"