#!/usr/bin/env python3

"""

   GPX Analytics Code base 


"""

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2019, Juan M. Huerta"

import sys
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps
from datetime import datetime
import operator
from math import radians, cos, sin, asin, sqrt
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math
from collections import namedtuple
#from gpx_analytics.segment_analytics import multi_sensor_point
#
#import gpx_analytics
#import gpx_analytics.segment_analytics
from  gpx_analytics.segment_analytics.multi_sensor_point import multi_sensor_point


import csv
try:
    from itertools import imap
except:
    imap = map

#from scipy import signal


class segment_analytics_object:

    
    def __init__(self):

       ##  Global Parameters
        
        self.filter_order = 24
        self.gap_order = 12
        self.gap_gain = 5.0


        ##  S : Sensor point array
        ##  X : offset lat-long points
        ##  Xd: Velocity Curve
        ##  Xf: Filtered velocity curve
        ##  HR: Heart Rate
        ##  P : Pace (Filtered)
        ## GAP : Grade Adjusted Pace

        self.S=[]
        self.X=None
        self.Xd=None
        self.Xf=None
        self.HR=None
        self.P=None
        self.G=None
        self.GAP=None

    def load_gpx(self,file_location):
        my_data = eval(dumps(bf.data(fromstring(open(file_location,'rt').read()))))
        a='{http://www.topografix.com/GPX/1/1}'
        X=[]
        md=None
        origin=None
        for p in my_data[a+"gpx"][a+"trk"][a+"trkseg"][a+"trkpt"]:
            datetime_object = datetime.strptime(p[a+"time"]['$'], '%Y-%m-%dT%H:%M:%SZ')
            if md is None or datetime_object < md:
                md = datetime_object
                origin =(float(p['@lat']),  float(p['@lon']))
            #X.append( [datetime_object,  float(p['@lat']), float(p[a+"ele"]['$']),  float(p['@lon'])])
            self.S.append( multi_sensor_point(datetime_object,  float(p['@lat']), float(p[a+"ele"]['$']),  float(p['@lon']),None,None))
            
       ##  Duplet of (time, coordinates) :  (time, lat, lon)                                                                                                                                        
       # X=[[(x[0]-md).total_seconds(),(x[1],x[3])] for x in X]
        X=[[(x.datetime-md).total_seconds(),(x.latitude,x.longitude,x.elevation)] for x in self.S]
        self.X=sorted(X,key=operator.itemgetter(0))



    def load_csv(self,file_location):
        print("READING CSV")
        with open(file_location, mode="rt") as infile:
            reader = csv.reader(infile)
            Data = namedtuple("Data", next(reader))
            time_origin = None
            for data in imap(Data._make, reader):
                try:
                    # This is the Tom Tom CSV
                    self.S.append(multi_sensor_point(float(data.time),float(data.lat),float(data.elevation),float(data.long),float(data.heartRate),float(data.speed)))
                except:
                    if True: 
                        # This is the Garmin CSV:
                        datetime_object = datetime.strptime(data.timestamp, '%Y-%m-%d %H:%M:%S-06:00')
                        if time_origin is None:
                            time_origin = datetime_object
                        this_offset=(datetime_object-time_origin).total_seconds()    
                        #print(this_offset)
                        self.S.append(multi_sensor_point(this_offset,float(data.position_lat),float(data.altitude),float(data.position_long),None,None))
                        
                    else:
                        print("ERROR reading point:", data, "IGNORING")
        X=[[x.time_offset,(x.latitude,x.longitude,x.elevation)] for x in self.S]
        self.X=sorted(X,key=operator.itemgetter(0))



    def analyses(self,analysis_string):
        
                                                                                                                                                                                                
    # RAW_VELOCITY
    # FILTERED_VELOCITY
    # FILTERED_PACE 
    # LOG_POWER_SPECTRUM 
    # SPECTROGRAM
    # HEART_RATE_CURVE                                                                                                                                                                      
    # HR_PACE_SCATTER
    # ELEVATION
    # GAP

        good_analyses=set(["RAW_VELOCITY","FILTERED_VELOCITY","FILTERED_PACE","LOG_POWER_SPECTRUM","SPECTROGRAM","HEART_RATE_CURVE","HR_PACE_SCATTER","ELEVATION","GAP"])
        requests=sorted(good_analyses.intersection(set(analysis_string.split("|"))))
        for request in requests:
            print("PERFORMING ->", request)
            
        if len(requests) < 1 or len(requests)>5:
            print("ERROR: TOO MANY OR TOO FEW VALID ANALYSES")
            print("Valid analyses:")
            for valid in good_analyses:
                print("\t", valid)
            return


        self.compute_velocity()
        self.filter_velocity_and_pace()
        self.compute_power_spectrum()
        self.compute_heart_rate()
        self.compute_pace()

        if "GAP" in requests:
            self.compute_gap()

        self.make_plots(requests)
   

    def compute_velocity(self):
        self.Xd=[0.0]*len(self.X)
        for i in range(len(self.X)):
            if i == 0:
                self.Xd[i]=(0.0,0.0)
            else:
                self.Xd[i]=(self.X[i][0],self.my_haversine(self.X[i][1][1],self.X[i][1][0],self.X[i-1][1][1],self.X[i-1][1][0])/(self.X[i][0]-self.X[i-1][0]))

    def compute_heart_rate(self):
        HR=[(x.time_offset,x.heart_rate) for x in self.S ]
        self.HR=sorted(HR,key=operator.itemgetter(0))

                
    def filter_velocity_and_pace(self):
           moving_average  = self.filter_order
           Xf=[]
           just_X=[]
           just_X_pace=[]
           for k in range(len(self.Xd)-moving_average):
               x1 = sum([x[1] for x in self.Xd[k:k+moving_average]])/float(moving_average)
               Xf.append((self.X[k][0],x1))
               just_X.append(x1)
               just_X_pace.append(1.0/x1)
           self.just_X = np.array(just_X)
           self.just_X_pace=just_X_pace
           self.Xf=Xf

    def compute_pace(self):
           moving_average  = self.filter_order
           Xp=[]
           for k in range(len(self.Xd)-moving_average):
               x1 = sum([x[1] for x in self.Xd[k:k+moving_average]])/float(moving_average)
               Xp.append((self.X[k][0],1.0/x1))
           self.P=Xp

    def compute_grade(self):
        ## Todo: work in progress
        Xg=[]
        moving_average = self.gap_order
        x1=0.0
        for k in range(len(self.Xd)-moving_average):
            for i in range(moving_average):
                x1+=(1.0/float(moving_average))*(self.S[k].elevation-self.S[k+1].elevation)
            Xg.append(x1)
        self.G=Xg
        return


    def compute_gap(self):

        # TODO: https://medium.com/strava-engineering/improving-grade-adjusted-pace-b9a2a332a5dc
        ## TODO:
        ## Lets start with a poor mans version: A simple Velocity divided by grade           moving_average  = m_a

           Xp=[]
           self.compute_grade()
           moving_average = self.filter_order
           for k in range(len(self.Xd)-moving_average):
               x1 = sum([x[1] for x in self.Xd[k:k+moving_average]])/float(moving_average)
               Xp.append((self.X[k][0],1.0/x1 + self.gap_gain * self.G[k]))
           self.GAP=Xp




    def compute_power_spectrum(self):
        #  Log-Power Spectrum                                                                                                                                                                   
        self.ps = np.log(np.abs(np.fft.fft(self.just_X_pace))**2)



    def make_plots(self,analyses):
        #Plotting steps.                                                                                                                                                                        
        # Points are NOT evenly spaced, but let's ignore that fact for now                                                                                                                      
        plt.figure(1)
        n_panels = len(analyses)
        i=0
        for request in analyses:
            i+=1
            plt.subplot(n_panels,1,i)
            if request =="ELEVATION":
                plt.title("Raw Elevation points")
                plt.plot([x[0] for x in self.Xd], [x[1][2] for x in self.X], '-')
            elif request =="RAW_VELOCITY":
                plt.title("Raw velocity points")
                plt.plot([x[0] for x in self.Xd], [x[1] for x in self.Xd], '-')
            elif request == "FILTERED_VELOCITY":
                plt.title("Low-pass filtered velocity Curve")
                plt.plot([x[0] for x in self.Xf], [x[1] for x in self.Xf])
            elif request == "FILTERED_PACE":
                plt.title("Pace  Curve ")
                pc =[1.0/x[1] for x in self.Xf]
                plt.plot([x[0] for x in self.Xf],pc)
                plt.ylim(max(pc),min(pc))
            elif request == "GAP":
                plt.title("Grade Adjusted Pace (v0.0) ")
                gc =[x[1] for x in self.GAP]
                plt.plot([x[0] for x in self.GAP],gc)
                plt.ylim(max(gc),min(gc))
            elif request == "LOG_POWER_SPECTRUM":
                plt.title("Log Power Spectrum of the Whole Velocity Run")
                plt.plot(self.ps)
            elif request == "SPECTROGRAM":            
                NFFT = 64  # the length of the windowing segments
                plt.title("Changing Log Power Spectrum (Spectrogram)")
                x=[x[1] for x in self.Xf]
                x_p=[1.0/x[1] for x in self.Xf]
                Pxx, freqs, bins, im = plt.specgram(x_p, NFFT=NFFT, Fs=1.0, noverlap=0 )
            elif request == "HEART_RATE_CURVE":
                plt.title("Heart Rate")
                plt.plot([x[0] for x in self.HR], [x[1] for x in self.HR], '-')
            elif request == "HR_PACE_SCATTER":
                plt.title("HR_PACE_SCATTER")
                HR_P = [(1.0/x.speed,x.heart_rate) for x in self.S if x.speed > 0.0]
                plt.scatter([x[0] for x in HR_P],[x[1] for x in HR_P]),'.'

        self.seaborn_plots()
        plt.show()
        
    def seaborn_plots(self):
        if  sum([1.0 for x in self.S if x.speed is not None])>20:
            plt.figure(2)
            sns.set(style="whitegrid")
            data = pd.DataFrame([(1000.0*x[0][1], x[1].speed )for x in zip(self.Xf,self.S)],[x[0] for x in self.Xf],columns=['Calculated  Velocity (Filtered)','Device Speed'])
            sns.lineplot(data=data, palette="tab10", linewidth=2.5)
        


    def euclidean(self,x,y):
        return math.sqrt((x[0]-y[0])**2.0+(x[1]-y[1])**2.0)


    def my_haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
    # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles
        return c * r

