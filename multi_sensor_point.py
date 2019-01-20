#!/usr/bin/env python                                                                                                                                                                            
"""

Multi Sensor Point class

"""

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2019, Juan M. Huerta"


class multi_sensor_point:

    def __init__(self,dt,lat,ele,lon,heartRate,speed):
        self.latitude=lat
        self.longitude=lon
        self.datetime=dt
        self.speed = speed
        self.elevation=ele
        self.heart_rate=heartRate
        self.time_offset=dt

