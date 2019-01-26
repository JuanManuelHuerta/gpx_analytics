
#!/usr/bin/env python

"""

    v00.py: Creates a segment_analytics_object and invokes analysis steps

    Analysis|Display:
    
    RAW_VELOCITY
    FILTERED_VELOCITY
    FILTERED_PACE
    LOG_POWER_SPECTRUM
    SPECTROGRAM
    HEART_RATE_CURVE
    HR_PACE
    GAP

    To do:
    VO2_MAX_CURVE  (Cooper)
    RUNNING_POWER
    FTP




"""

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2019, Juan M. Huerta"

import sys
import gpx_analytics
import gpx_analytics.segment_analytics
import gpx_analytics.segment_analytics.segment_analytics_object
#import  gpx_analytics.segment_analytics.segment_analytics_object from gpx_analytics.segment_analytics
#from gpx_analytics.segment_analytics import  segment_analytics_object


def do_Analysis():

    file_name=None
    my_segment = gpx_analytics.segment_analytics.segment_analytics_object.segment_analytics_object()

    ##  
    if len(sys.argv) != 3:
        print("ERROR: argument(s) missing.\n USE:  v00.py  <FILE_NAME>  <ANALYSES>")
        print("RAW_VELOCITY|FILTERED_VELOCITY|FILTERED_PACE|LOG_POWER_SPECTRUM|SPECTROGRAM|HEART_RATE_CURVE|HR_PACE|HR_PACE_SCATTER|GAP")
        return 


    if len(sys.argv)==3  and 'gpx' in sys.argv[1]:
        file_name = sys.argv[1]
        my_segment.load_gpx(file_name)
    elif len(sys.argv)==3  and 'csv' in sys.argv[1]:
        file_name = sys.argv[1]
        my_segment.load_csv(file_name)
    else:
        print("No valid file specified")
        return

    my_segment.analyses(sys.argv[2])
    return 


if __name__ == "__main__":
    do_Analysis()

