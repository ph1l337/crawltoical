import requests
import time
import pytz
from icalendar import Calendar, Event, vText
from lxml import html
from dateutil.parser import parse
from datetime import timedelta
from dateutil.tz import gettz


def parse_calendar():
    cal = Calendar()
    cal.add('prodid', 'Brought to you by ph1l337')
    cal.add('version', '2.0')

    res = requests.get(
        'https://www.kth.se/en/ece/avdelningen-for-larande/sprak-och-kommunikation/for-studenter/for-master-och-utbytesstudenter/introduktionskurs')
    tree = html.fromstring(res.content)
    rows = tree.xpath('//table/tr')

    for row in rows[1:]:
        columns = row.xpath('td/text()')
        event = Event()
        event.add('summary', 'Swedish Class')

        tzinfos = {"CEST": pytz.timezone("Europe/Stockholm")}
        start = parse('{} {}:00 CEST'.format(columns[2], columns[3]), tzinfos=tzinfos) - timedelta(hours=2)
        end = parse('{} {}:00 CEST'.format(columns[2], columns[4]), tzinfos=tzinfos) - timedelta(hours=2)
        event.add('dtstart', start)
        event.add('dtend', end)
        event['location'] = vText(columns[5])

        cal.add_component(event)

    with open('out/swedish_course.ics', 'wb') as f:
        f.write(cal.to_ical())


if __name__ == '__main__':
    while True:
        parse_calendar()
        time.sleep(3600)
