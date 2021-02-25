import sys
from io import BytesIO

import requests

from constants import GEOCODE_APIKEY


def request_error(response):
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    print('Content:\n%s' % response.text)
    sys.exit(1)


def get_image(coords, map_type, scale=None, size=None, mark=None):
    basic = 'https://static-maps.yandex.ru/1.x/'
    params = {'ll': ','.join(map(str, coords)),
              'l': map_type}
    if scale:
        params['z'] = scale
    if mark:
        params['pt'] = f'{mark["coords"]},{mark["type"]}{mark["color"]}{mark["size"]}'
    if size:
        params['spn'] = ','.join(map(str, size))
    response = requests.get(basic, params=params)
    if not response:
        request_error(response)
    return BytesIO(response.content)


def get_geo_object(geocode: str):
    geocode_url = 'http://geocode-maps.yandex.ru/1.x/'
    geocode_error_msg = 'Не удалось найти объект на карте'
    response = requests.get(geocode_url, params={'geocode': geocode,
                                                 'format': 'json',
                                                 'results': 1,
                                                 'apikey': GEOCODE_APIKEY})

    if not response:
        request_error(response)
    data = response.json()['response']
    results = data['GeoObjectCollection']['featureMember']
    if not results:
        return geocode_error_msg
    return results[0]['GeoObject']


def get_toponym_scale(toponym):
    lower_corner, upper_corner = map(lambda x:
                                     tuple(map(float, toponym['boundedBy']['Envelope'][x].split())),
                                     ['lowerCorner', 'upperCorner'])
    return abs(upper_corner[0] - lower_corner[0]), abs(upper_corner[1] - lower_corner[1])


def extract_coords(toponym):
    return list(map(float, toponym['Point']['pos'].split()))
