import argparse
import json
import os
from math import floor
from time import time

import boto3
import requests

r2 = boto3.resource('s3',
    endpoint_url = f"https://{os.environ['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com",
    aws_access_key_id = os.environ['CLOUDFLARE_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['CLOUDFLARE_SECRET_ACCESS_KEY']
)
bucket = r2.Bucket('totally-wanderlost')

def load_existing_data(path):
    # TODO: check exists first and return empty structure if not
    return json.load(open(path, 'rb'))

def update_data_file(path, data):
    with open(path, 'wb') as file:
        encoded = json.dumps(data, indent=4).encode()
        file.write(encoded)

def fetch_latest_data(trip_id):
    data = fetch(trip_id)

    visited = [ step for step in parse_steps(data['all_steps']) ]
    visited[-1]['state'] = 'current'
    planned = [ step for step in parse_planned_steps(data['planned_steps']) ]

    return {
        'steps': visited + planned
    }

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
                'name': encode(step['name']) if not empty(step['name']) else step['location']['name'],
                'description': encode(step['description']) if not empty(step['description']) else None,
                'country': step['location']['detail'],
                'arrived': floor(step['start_time']),
                'location': [step['location']['lat'], step['location']['lon']],
                'photos': [ get_photo(step, item) for item in step['media'] if 'large_thumbnail_path' in item and not empty(item['large_thumbnail_path']) ],
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
            'name': encode(step['location']['name']),
            'country': step['location']['detail'],
            'arrived': False,
            'location': [step['location']['lat'], step['location']['lon']],
            'photos': [],
            'state': 'planned'
        }

def empty(string):
    return string == None or string == ''

def encode(unicode):
    return unicode.encode('ascii', 'xmlcharrefreplace').decode('utf8')

def get_photo(step, photo):
    source_url = photo['large_thumbnail_path']
    imagekit_url = f"https://ik.imagekit.io/totallywanderlost/r2/{r2_key_for_photo(step['uuid'], photo['uuid'])}"

    return {
        'id': photo['uuid'],
        'source_url': source_url,
        'r2_url': r2_url_for_photo(step['uuid'], photo['uuid']),
        'url': imagekit_url,
        'location': [photo['lat'], photo['lon']]
    }

def r2_key_for_photo(step_id, photo_id):
    return f"images/journey/step/{step_id}/{photo_id}"

def r2_url_for_photo(step_id, photo_id):
    return f"https://r2.totallywanderlost.com/{r2_key_for_photo(step_id, photo_id)}"

def upload_photo(source_url, key, step_id):
    print(f"Downloading source photo={source_url} for step={step_id}")
    source = requests.get(source_url)

    print(f"Uploading photo with key={key} to r2 for step={step_id}")
    bucket.Object(key).put(Body=source.content)

def delete_photo(step_id, photo_id):
    key = r2_key_for_photo(step_id, photo_id)

    print(f"Deleting photo with key={key} from r2 for step={step_id}")
    bucket.Object(key).delete()

def sync_images_to_r2(existing, latest):
    existing_by_id = {step['id']: step for step in existing['steps']}
    latest_by_id = {step['id']: step for step in latest['steps']}

    synced = []
    for id, step in latest_by_id.items():
        existing_step = existing_by_id[id] if id in existing_by_id else None
        existing_photos_by_id = {photo['id']: photo for photo in existing_step['photos']} if existing_step else dict()

        for photo in step['photos']:
            if photo['id'] not in existing_photos_by_id:
                print(f"Uploading new photo with id={photo['id']} for step={step['id']}")
                key = r2_key_for_photo(step['id'], photo['id'])
                upload_photo(photo['source_url'], key, step['id'])

        synced.append(step)

    for id, step in existing_by_id.items():
        latest_step = latest_by_id[id] if id in latest_by_id else None
        latest_photos_by_id = {photo['id']: photo for photo in latest_step['photos']} if latest_step else dict()

        for photo in step['photos']:
            if photo['id'] not in latest_photos_by_id:
                print(f"Deleting photo with id={photo['id']} for step={step['id']}")
                delete_photo(step['id'], photo['id'])

    return {
        'steps': synced
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data from Polarsteps')
    parser.add_argument('-t', '--trip', required=True, dest='trip', type=int, help='Polarsteps trip id')
    parser.add_argument('-f', '--file', required=True, dest='file', help='File path to write data to')
    args = parser.parse_args()

    existing = load_existing_data(args.file)
    latest = fetch_latest_data(args.trip)
    synced = sync_images_to_r2(existing, latest)

    update_data_file(args.file, synced)
