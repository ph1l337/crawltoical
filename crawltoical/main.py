import requests
from lxml import html
from ics import Calendar, Event


def parse_calendar():

    calendar = Calendar()
    res = requests.get('https://www.kth.se/en/ece/avdelningen-for-larande/sprak-och-kommunikation/for-studenter/for-master-och-utbytesstudenter/introduktionskurs')
    tree = html.fromstring(res.content)
    rows = tree.xpath('//table/tr')

    for row in rows[1:]:
        columns = row.xpath('td/text()')
        e = Event()
        e.name = "Swedish Class"
        e.begin = ('{} {}'.format(columns[2], columns[3]), 'YYYY-MM-DD HH:mm')
        e.end = ('{} {}'.format(columns[2], columns[4]), 'YYYY-MM-DD HH:mm')
        e.location = columns[5]

        calendar.events.append(e)

    with open('out/swedish_course.ics', 'w') as f:
        f.writelines(calendar)


if __name__ == '__main__':
    parse_calendar()

