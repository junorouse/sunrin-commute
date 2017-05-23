import xml.etree.ElementTree as ET
import re
from requests import get

bus_url = 'http://bus.go.kr/xmlRequest/getStationByUid.jsp?strBusNumber=02004'
metro_url = 'http://bus.go.kr/getSubway_6.jsp?statnId=1001000133&subwayId=1001'

bus_tree = ET.fromstring(get(bus_url).content.strip())

expected_bus = ['162', '505', '503', '7016']
'''
best: 162, 503, 7016
good: 505
'''
bus_arrival = []

for bus in bus_tree.iter('stationList'):
    try:
        bus_id = expected_bus[expected_bus.index(bus.find('rtNm').text)]
        first = bus.find('arrmsg1').text
        m = re.match('\d분', first)
        bus_arrival.append({
            'bus_id': bus_id,
            'remain_time': first
        })
    except ValueError:
        continue
