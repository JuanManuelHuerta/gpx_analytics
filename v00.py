
import sys
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps

my_data = eval(dumps(bf.data(fromstring(open('2007129462.gpx','rt').read()))))
a='{http://www.topografix.com/GPX/1/1}'


for p in my_data[a+"gpx"][a+"trk"][a+"trkseg"][a+"trkpt"]:
    print (p[a+"time"]['$'],  float(p['@lon']), float(p[a+"ele"]['$']),  float(p['@lat']))


    
