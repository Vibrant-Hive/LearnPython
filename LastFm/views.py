from django.shortcuts import render
import requests
import json
import requests_cache

import time
from IPython.core.display import clear_output

API_KEY = '827d80b165f4a47048514195f435b8c9'
USER_AGENT = 'VibrantHive'

requests_cache.install_cache()
responses = []


def get_top_artists(request):
    call_api()
    context = {'response': responses}
    return render(request, 'base.html', context)


def call_api():
    page = 1
    total_pages = 99999

    while page <= total_pages:
        payload = {
            'method': 'chart.gettopartists',
            'limit': 500,
            'page': page
        }

        # print some output so we can see the status
        print("Requesting page {}/{}".format(page, total_pages))
        # clear the output to make things neater
        clear_output(wait=True)

        # make the API call
        response = lastfm_get(payload)

        # if we get an error, print the response and halt the loop
        if response.status_code != 200:
            print(response.text)
            break

        # extract pagination info
        page = int(response.json()['artists']['@attr']['page'])
        total_pages = int(response.json()['artists']['@attr']['totalPages'])

        # append response
        responses.append(response)

        # if it's not a cached result, sleep
        if not getattr(response, 'from_cache', False):
            time.sleep(0.25)

        # increment the page number
        page += 1


def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
