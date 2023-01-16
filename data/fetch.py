import argparse
import json
from math import floor
from time import time

import requests


def update_data_file(trip_id, path):
    data = {}
    data['steps'] = get_steps(trip_id)

    with open(path, 'wb') as file:
        contents = json.dumps(data, indent=4)
        file.write(contents.encode())

def get_steps(trip_id):
    data = fetch(trip_id)

    visited = [ step for step in parse_steps(data['all_steps']) ]
    visited[-1]['state'] = 'current'
    planned = [ step for step in parse_planned_steps(data['planned_steps']) ]

    return visited + planned

def fetch(trip_id):
    response = requests.get(f'https://api.polarsteps.com/trips/{trip_id}')

    return response.json()

def parse_steps(steps):
    for step in steps:
        if step['is_deleted'] == True:
            continue

        if 'supertype' in step and step['supertype'] == 'normal':
            yield {
                'id': step['uuid'],
                'name': step['name'] if not empty(step['name']) else step['location']['name'],
                'country': step['location']['detail'],
                'arrived': floor(step['start_time']),
                'location': [step['location']['lat'], step['location']['lon']],
                'photos': [ get_photo(item) for item in step['media'] if 'large_thumbnail_path' in item and not empty(item['large_thumbnail_path']) ],
                'state': 'visited' if len(step['media']) > 0 else 'stopped'
            }

def parse_planned_steps(steps):
    now = int(time())

    for step in list(reversed(steps)):
        if step['is_deleted'] == True:
            continue

        if not empty(step['visit_time']):
            continue

        if not empty(step['start_time']) and step['start_time'] < now:
            continue

        yield {
            'id': step['uuid'],
            'name': step['location']['name'],
            'country': step['location']['detail'],
            'arrived': False,
            'location': [step['location']['lat'], step['location']['lon']],
            'photos': [],
            'state': 'planned'
        }

def empty(string):
    return string == None or string == ''

def get_photo(item):
    s3_url = item['large_thumbnail_path']
    s3_path = s3_url.replace('https://polarsteps.s3.amazonaws.com', '')
    imagekit_url = f'https://ik.imagekit.io/totallywanderlost/{s3_path}'

    return {
        'source_url': s3_url,
        'url': imagekit_url,
        'location': [item['lat'], item['lon']]
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from Polarsteps')
    parser.add_argument('-t', '--trip', required=True, dest='trip', type=int, help='Polarsteps trip id')
    parser.add_argument('-f', '--file', required=True, dest='file', help='File path to write data to')
    args = parser.parse_args()

    update_data_file(args.trip, args.file)
