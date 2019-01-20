#!/usr/bin/env python                                                                                                                                                                            
"""

Multi Sensor Point class

"""

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2019, Juan M. Huerta"


class multi_sensor_point:

    def __init__(self,dt,lat,ele,lon):
        self.latitude=lat
        self.longitude=lon
        self.datetime=dt
        self.elevation=ele
        self.heartrate=None
        self.time_offset=dt

