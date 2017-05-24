import xml.etree.ElementTree as ET
import re
from operator import itemgetter
from requests import get


def get_transport_arrival():
    bus_url = 'http://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=02004'
    metro_url = 'http://bus.go.kr/getSubway_6.jsp?statnId=1001000133&subwayId=1001'

    bus_tree = ET.fromstring(get(bus_url).content.strip())

    expected_bus = ['162', '505', '503', '7016']
    '''
    best: 162, 503, 7016
    good: 505
    '''
    transport_arrival = []

    for bus in bus_tree.iter('stationList'):
        try:
            bus_id = expected_bus[expected_bus.index(bus.find('rtNm').text)]
            first = bus.find('arrmsg1').text
            if first == '곧 도착':
                remain_minute = 0
                remain_stop = str(0)
            else:
                m = re.search("(\d+)분.+\[(\d)", first)
                try:
                    remain_minute = m.group(1)
                    remain_stop = m.group(2)
                except AttributeError:
                    continue

            if bus_id == '505':
                desc = '차 밀림'
            else:
                desc = '좋음'

            transport_arrival.append({
                'trasport_id': bus_id,
                'remain_minute': int(remain_minute),
                'remain_stop': remain_stop,
                'color': '#ACE7FF',
                'desc': desc
            })
        except ValueError:
            continue

    metro_data = get(metro_url).content.decode('utf-8')

    first_metro = metro_data.split('<div class="arvl1"><font color="red" size="2" style="font-weight:bold">이번열차 : ')[1].split('</font>')[0]
    try:
        second_metro = metro_data.split('<p>다음열차 : ')[1].split('<br/>')[0]
        is_second_metro = True
    except IndexError:
        is_second_metro = False

    first_remain_stop = ''

    if first_metro.startswith('전역'):
        if first_metro == '전역 도착':
            first_remain_minute = 0
        else:
            first_remain_minute = -1
        first_remain_stop = first_metro
    else:
        m = re.search("(\d+)분", first_metro)
        first_remain_minute = m.group(1)

    transport_arrival.append({
        'trasport_id': 'metro',
        'remain_minute': int(first_remain_minute),
        'remain_stop': first_remain_stop,
        'color': '#FFABAB',
        'desc': '많이 걸음'
    })

    if is_second_metro:
        m = re.search("(\d+)분", second_metro)
        second_remain_minute = m.group(1)

        transport_arrival.append({
            'trasport_id': 'metro',
            'remain_minute': int(second_remain_minute),
            'remain_stop': '',
            'color': '#FFABAB',
            'desc': '많이 걸음'
        })

    transport_arrival = sorted(transport_arrival, key=itemgetter('remain_minute'))

    return transport_arrival
