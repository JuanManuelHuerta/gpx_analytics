#!/usr/bin/env python

"""v00.py: calculates my speed curve from a gpx file """

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2019, Juan M. Huerta"

import sys
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps
from datetime import datetime
import operator
from haversine import haversine
import numpy as np
import matplotlib.pyplot as plt
import math

def euclidean(x,y):
    return math.sqrt((x[0]-y[0])**2.0+(x[1]-y[1])**2.0)


my_data = eval(dumps(bf.data(fromstring(open('2007129462.gpx','rt').read()))))
a='{http://www.topografix.com/GPX/1/1}'


X=[]
md=None
origin=None
for p in my_data[a+"gpx"][a+"trk"][a+"trkseg"][a+"trkpt"]:
    datetime_object = datetime.strptime(p[a+"time"]['$'], '%Y-%m-%dT%H:%M:%SZ')
    if md is None or datetime_object < md:
        md = datetime_object
        origin =(float(p['@lat']),  float(p['@lon']))
    X.append( [datetime_object,  float(p['@lat']), float(p[a+"ele"]['$']),  float(p['@lon'])])

X=[[(x[0]-md).total_seconds(),(x[1],x[3])] for x in X]
X=sorted(X,key=operator.itemgetter(0))
        
Xd=[0.0]*len(X)
for i in range(len(X)):
    if i == 0:
        Xd[i]=(0.0,0.0)
    else:
        Xd[i]=(X[i][0],1000.0*haversine(X[i][1],X[i-1][1])/(X[i][0]-X[i-1][0]))
        #Xd[i]=(X[i][0],1000.0*euclidean(X[i][1],X[i-1][1])/(X[i][0]-X[i-1][0]))
        

# Filter speed 
moving_average  = 48
Xf=[]
for k in range(len(Xd)-moving_average):
    print k
    x1 = sum([x[1] for x in Xd[k:k+moving_average]])/float(moving_average)
    Xf.append((X[k][0],x1))
X=Xf





plt.figure(1)
plt.plot([x[0] for x in Xf], [x[1] for x in Xf], 'bo')
plt.show()


    
