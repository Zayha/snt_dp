import psycopg2
import requests
from datetime import datetime, timedelta
import auth_data


def get_data_from_api():
    headers = {
        'authorization': auth_data.hat
    }
    response = requests.get(auth_data.url_v, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def check_data(json_response) -> list:
    if json_response is not None:
        datetime_obj = datetime.fromisoformat(json_response['last_updated'])
        voltage = json_response['state']
        shifted_datetime = datetime_obj + timedelta(hours=3)
        return [voltage, shifted_datetime]
    else:
        return ['0.0', datetime.now().time()]


def send_data_to_db():
    pass


for i in get_data_from_api()[0]:
    print(i)
