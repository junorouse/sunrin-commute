import xml.etree.ElementTree as ET
import re
from operator import itemgetter
from requests import get

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
            remain_minute = str(0)
            remain_stop = str(0)
        else:
            m = re.search("(\d)분.+\[(\d)", first)
            try:
                remain_minute = m.group(1)
                remain_stop = m.group(2)
            except AttributeError:
                continue
        transport_arrival.append({
            'trasport_id': bus_id,
            'remain_minute': remain_minute,
            'remain_stop': remain_stop
        })
    except ValueError:
        continue


metro_data = get(metro_url).content.decode('utf-8')

first_metro = metro_data.split('<div class="arvl1"><font color="red" size="2" style="font-weight:bold">이번열차 : ')[1].split('</font>')[0]
second_metro = metro_data.split('<p>다음열차 : ')[1].split('<br/>')[0]

if first_metro.startswith('전역'):
    if first_metro == '전역 도착':
        first_remain_minute = str(0)
    else:
        first_remain_minute = str(-1)
    first_remain_stop = first_metro
else:
    m = re.search("(\d)분.+\((\w+)\)", first_metro)
    first_remain_minute = m.group(1)
    first_remain_stop = m.group(2)

m = re.search("(\d)분.+\((\w+)\)", second_metro)
second_remain_minute = m.group(1)
second_remain_stop = m.group(2)


transport_arrival.append({
    'trasport_id': 'metro',
    'remain_minute': first_remain_minute,
    'remain_stop': first_remain_stop
})

transport_arrival.append({
    'trasport_id': 'metro',
    'remain_minute': second_remain_minute,
    'remain_stop': second_remain_stop
})
# [{'remain_minute': '0', 'trasport_id': '162', 'remain_stop': '0'}, {'remain_minute': '3', 'trasport_id': '503', 'remain_stop': '9'}, {'remain_minute': '4', 'trasport_id': '505', 'remain_stop': '2'}, {'remain_minute': '6', 'trasport_id': 'metro', 'remain_stop': '종각'}, {'remain_minute': '7', 'trasport_id': 'metro', 'remain_stop': '종로3가'}]
transport_arrival = sorted(transport_arrival, key=itemgetter('remain_minute'))
