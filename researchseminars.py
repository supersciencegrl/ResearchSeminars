''' Code from https://researchseminars.org/api/ '''

import requests
import warnings

warnings.simplefilter('ignore', requests.packages.urllib3.exceptions.InsecureRequestWarning) # Hide warnings from verify = False

def get_topics(subject):
    # Default subject = 'chem'
    url = 'https://researchseminars.org/api/0/topics'
    r = requests.get(url, verify = False)
    if r.status_code == 200:
        topics = r.json()[subject]
        return topics

def authorization():
    with open('apitoken.txt') as tokenfile:
        apitoken = tokenfile.read().strip()
    domain = 'syngenta.com' # Avoid email harvesting

    return f'nessa.carson@{domain} {apitoken}'

def lookup_talk(seriesName):
    url = f'https://researchseminars.org/api/0/lookup/series?series_id="{seriesName}"'
    r = requests.get(url, verify = False)
    if r.status_code == 200:
        json = r.json()
        properties = json['properties']
        try:
            print(properties['name'], properties['start_date'])
        except TypeError: #NoneType
            print('Talk not found')

def create_seminar_series(series_id, name, topics, slots, organizers, eventurl, **kwargs):
    if 'is_conference' in kwargs:
        is_conference = kwargs['is_conference']
    else:
        is_conference = False
    print(is_conference)

    url = 'https://researchseminars.org/api/0/save/series'
    payload = {'series_id': series_id,
               'name': name,
               'is_conference': is_conference,
               'topics': topics,
               'language': 'en',
               'institutions': [],
               'timezone': 'Europe/London',
               'visibility': 2,
               'access_control': 0,
               'slots': slots,
               'organizers': [{'name': organizers,
                               'email': '',
                               'homepage': eventurl,
                               'order': 0,
                               'display': True}]
               }

    r = requests.post(url, json = payload, headers = {'authorization': authorization()}, verify = False)
    json = r.json()
    code = json.get('code')

    if r.status_code == 200:
        if code == 'warning':
            print(f'Created with warnings: {json["warnings"]}')
        else:
            print('Event created successfully. ')
    else:
        print(f'Event creation failed. \n{json}')

def newseries(**kwargs):
    series_id = input('Series ID (with underscores): ')
    name = series_id.replace('_', ' ').capitalize()
    topics = input('Topics (comma-separated): ')
    topics = ['chem'] + topics.replace(', ', ',').split(',')
    slots = input('Slots (comma-separated): ')
    slots = slots.replace(', ', ',').split(',')
    organizers = input('Organizer(s): ')
    eventurl = input('Event url: ')
    if not eventurl.startswith('http'):
        eventurl = 'http://' + eventurl

    create_seminar_series(series_id, name, topics, slots, organizers, eventurl, **kwargs)

def newconference():
    newseries(is_conference = True)

# Can you add title and time here, I dunno
def create_talk(series_id):
    url = 'https://researchseminars.org/api/0/save/talk/'
    payload = {'series_id': series_id}
    r = requests.post(url, json = payload, headers = {'authorization': authorization()})
    json = r.json()
    code = json.get('code')

    if r.status_code == 200:
        if code == 'warning':
            print(f'Created talk for series_ctr {json["series_ctr"]} with warnings {json["warnings"]}')
        else:
            print(f'Created talk for series_ctr {json["series_ctr"]} successfully.')
    else:
        print(f'Talk creation failed. \n{json}')
    













    
