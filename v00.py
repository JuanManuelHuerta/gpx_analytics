#!/usr/bin/env python

"""

    v00.py: Creates a segment_analytics_object and invokes analysis steps

"""

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2019, Juan M. Huerta"

import sys
import gpx_analytics

def do_Analysis():

    file_name=None
    if len(sys.argv)>1 and sys.argv[1]!=None:
        file_name = sys.argv[1]
    else:
        file_name = 'data/2007129462.gpx'

    my_segment = gpx_analytics.segment_analytics_object()
    my_segment.load_gpx(file_name)
    my_segment.compute_velocity()
    my_segment.filter_velocity(24)
    my_segment.compute_power_spectrum()
    my_segment.make_plots()



if __name__ == "__main__":
    do_Analysis()

