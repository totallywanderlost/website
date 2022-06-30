import argparse
import json

import requests


def update_data_file(trip_id, path):
    data = {}
    data['pins'] = get_pins(trip_id)

    with open(path, 'wb') as file:
        contents = json.dumps(data, indent=4)
        file.write(contents.encode())

def get_pins(trip_id):
    data = fetch(trip_id)
    steps = data['all_steps']

    return [ get_pin(step) for step in steps]

def fetch(trip_id):
    response = requests.get(f'https://api.polarsteps.com/users/byusername/totallywanderlost')
    trips = [trip for trip in response.json()['alltrips'] if trip['id'] == trip_id]

    return trips[0]

def get_pin(step):
    return {
        'name': step['location']['name'],
        'location': [step['location']['lat'], step['location']['lon']]
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from Polarsteps')
    parser.add_argument('-t', '--trip', required=True, dest='trip', type=int, help='Polarsteps trip id')
    parser.add_argument('-f', '--file', required=True, dest='file', help='File path to write data to')
    args = parser.parse_args()

    update_data_file(args.trip, args.file)
