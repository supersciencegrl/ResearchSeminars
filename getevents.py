''' Much of this comes from website-tools/events_from_html.py, which is more likely to be in a
    better state of update '''

import datetime
from dateutil import tz
import urllib.request
import urllib.error

def check_html_is_list(html):
    if type(html) is str:
        htmllist = html.split('\n')
    else:
        htmllist = html

    return htmllist

def gettimezone(time_line):
    vtimezone = time_line.split('<td class="columnb2">')[1].split(' ')[1].split('</td>')[0]
    if vtimezone == 'BST':
        result = London
    else:
        result = tz.gettz() # Returns tzlocal

    return result

def pullwebinar(html, startpos):
    htmllist = check_html_is_list(html)
    print(startpos)

    event = {}
    for n, line in [(m, longline.lstrip()) for m, longline in enumerate(htmllist[startpos:])]:
        if line.startswith('<tr class="covidrow'):
            event = {'linestart': n + startpos, 'enddate': False, 'allday': False}
        # Event dates
        elif line.startswith('<td class="columnb1'):
            wholedate = line.split('<td class="columnb1">')[1].split('</td>')[0].replace('&nbsp;', ' ')
            if any(('-' in wholedate, '&ndash;' in wholedate)):
                date = wholedate.split('&ndash;')[0].split('-')[0]
                enddate = wholedate.split('&ndash;')[-1].split('-')[-1]
                event['enddate'] = datetime.datetime.strptime(enddate, '%a %d/%m/%Y')
            else:
                date = wholedate

        # Event times
        elif line.startswith('<td class="columnb2'):
            event['timezone'] = gettimezone(line)
            if 'all day' in line.lower():
                event['allday'] = True
                event['starttime'] = datetime.datetime.strptime(date, '%a %d/%m/%Y')
            else:
                wholetime = line.split('<td class="columnb2">')[1].split(' BST')[0].replace('&#8209;', '-')
                vstarttime = wholetime.split('&ndash;')[0].split('-')[0].split(' ')[0]
                if any(('&ndash;' in wholetime, '-' in wholetime)):
                    vendtime = wholetime.split('-')[-1].split('&ndash;')[-1].split(' ')[0]
                else:
                    vendtime = None

                event['starttime'] = datetime.datetime.strptime(f'{date} {vstarttime}', '%a %d/%m/%Y %H:%M').replace(tzinfo = event['timezone'])
                if vendtime:
                    event['endtime'] = datetime.datetime.strptime(f'{date} {vendtime}', '%a %d/%m/%Y %H:%M').replace(tzinfo = event['timezone'])
                else:
                    event['endtime'] = None

        elif line.startswith('<td class="columnb3'):
            event['url'] = line.split('<td class="columnb3"><a href="')[1].split('"')[0]

            description = []
            for nextline in [longnextline.strip() for longnextline in htmllist[startpos+n+1:]]:
                if not nextline.startswith('<td'):
                    description.append(nextline.replace('<br>', '\n'))
                else: # When you reach the end
                    descriptionstring = ('').join(('').join(description).split('</a>'))
                    event['title'] = descriptionstring.split('</a>')[0].split('\n')[0].split(' (')[0]
                    event['eventtype'] = descriptionstring.split('(')[-1].split(',')[-1].split('</')[0].replace('&nbsp;', ' ').replace(')', '')
                    break

        elif line.startswith('<td class="columnb4'):
            event['organizer'] = line.split('<td class="columnb4">')[1].split('</td>')[0]

        elif line.startswith('</tr>'):
            event['lineend'] = n + startpos
            break

    return event

def allevents(html):
    htmllist = check_html_is_list(html)

    firsteventfound = False
    lasteventfound = False
    eventcount = 0
    for n, row in enumerate(htmllist):
        if row.lstrip().startswith('<tr class="covidrow'):
            eventcount += 1
            firsteventfound = True
            event = pullwebinar(htmllist, n)
            lod.append(event)

        elif row.lstrip().startswith('</tbody>'):
            lasteventfound = True
    print('Event count:', eventcount)

def getoldevents():
    url = 'http://supersciencegrl.co.uk/online-old'

    try:
        with urllib.request.urlopen(url) as response:
            htmlr = response.readlines()
    except urllib.error.HTTPError as error:
        print(error.code, error.read)
    
    global html_old
    html_old = []
    errors_old = []
    for h in htmlr:
        try:
            html_old.append(h.decode('utf-8'))
        except UnicodeDecodeError:
            errors_old.append(h)

    if html_in:
        print(f'Loaded {url} successfully as html_old.')

# Time zones
London = tz.gettz('Europe/London')

url = 'http://supersciencegrl.co.uk/online'

try:
    with urllib.request.urlopen(url) as response:
        htmlr = response.readlines()
except urllib.error.HTTPError as error:
    print(error.code, error.read)

html_in = []
errors = []
for h in htmlr:
    try:
        html_in.append(h.decode('utf-8'))
    except UnicodeDecodeError:
        errors.append(h)

if html_in:
    print(f'Loaded {url} successfully.')
lod = []
