import os
import sys
from io import BytesIO

import requests


def request_error(response):
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    print('Content:\n%s' % response.text)
    sys.exit(1)


def get_image(params):
    basic = 'https://static-maps.yandex.ru/1.x/'
    request_params = {'ll': ','.join(map(str, params['coords'])),
                      'l': params['map_type'], 'z': params['z']}
    if 'mark' in params.keys():
        mark = params['mark']
        request_params['pt'] = '%s,%s%s%s' % (mark['coords'], mark['type'], mark['color'], mark['size'])
    response = requests.get(basic, params=request_params)
    if not response:
        request_error(response)
    return BytesIO(response.content)


def get_geo_object(geocode: str):
    geocode_url = 'http://geocode-maps.yandex.ru/1.x/'
    geocode_error_msg = 'Не удалось найти объект на карте'
    response = requests.get(geocode_url, params={'geocode': geocode,
                                                 'format': 'json',
                                                 'results': 1,
                                                 'apikey': os.environ['GEOCODE_APIKEY']})

    if not response:
        request_error(response)
    data = response.json()['response']
    results = data['GeoObjectCollection']['featureMember']
    if not results:
        return geocode_error_msg
    return results[0]['GeoObject']


def get_toponym_scale(toponym):
    lower_corner, upper_corner = [float(toponym['boundedBy']['Envelope'][x].split()[0])
                                  for x in ['lowerCorner', 'upperCorner']]
    size = round(abs(upper_corner - lower_corner), ndigits=3)
    z_translate = {(200, 250): 1, (150, 199.999): 2, (100, 149.999): 3,
                   (50, 99.999): 4, (25, 49.999): 5, (20, 24.999): 6,
                   (15, 19.999): 7, (7, 14.999): 8, (5, 6.999): 9,
                   (4, 4.999): 10, (2, 3.999): 11, (1, 1.999): 12,
                   (0.5, 0.999): 13, (0.25, 0.499): 14, (0.1, 0.249): 15,
                   (0.05, 0.999): 16, (0.005, 0.049): 17,
                   (0, 0.0049): 18}
    results = list(filter(lambda x: x[0][0] <= size <= x[0][1], z_translate.items()))
    return results[0][1] if results else None


def extract_coords(toponym):
    return list(map(float, toponym['Point']['pos'].split()))
