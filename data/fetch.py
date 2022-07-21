import argparse
import json
from math import floor

import requests


def update_data_file(trip_id, path):
    data = {}
    data['steps'] = get_steps(trip_id)

    with open(path, 'wb') as file:
        contents = json.dumps(data, indent=4)
        file.write(contents.encode())

def get_steps(trip_id):
    data = fetch(trip_id)

    visited = [ get_step(step) for step in data['all_steps'] if 'supertype' in step and step['supertype'] == 'normal' ]
    visited[-1]['state'] = 'current'
    planned = list(reversed([ get_planned_step(step) for step in data['planned_steps'] if step['visit_time'] == None ]))

    return visited + planned

def fetch(trip_id):
    response = requests.get(f'https://api.polarsteps.com/trips/{trip_id}')

    return response.json()

def get_step(step):
    return {
        'name': step['location']['name'],
        'arrived': floor(step['start_time']),
        'location': [step['location']['lat'], step['location']['lon']],
        'photos': [ get_photo(item) for item in step['media'] if 'path' in item and item['path'] != '' ],
        'state': 'visited'
    }

def get_planned_step(step):
    return {
        'name': step['location']['name'],
        'arrived': False,
        'location': [step['location']['lat'], step['location']['lon']],
        'photos': [],
        'state': 'planned'
    }

def get_photo(item):
    return {
        'url': item['path'],
        'location': [item['lat'], item['lon']]
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from Polarsteps')
    parser.add_argument('-t', '--trip', required=True, dest='trip', type=int, help='Polarsteps trip id')
    parser.add_argument('-f', '--file', required=True, dest='file', help='File path to write data to')
    args = parser.parse_args()

    update_data_file(args.trip, args.file)
