
#!/usr/bin/env python

"""

    v00.py: Merges 2 files


"""

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2019, Juan M. Huerta"

import sys
import gpx_analytics
import gpx_analytics.segment_analytics
import gpx_analytics.segment_analytics.segment_analytics_object
import gpx_analytics.algorithms
import gpx_analytics.algorithms.distances

#import  gpx_analytics.segment_analytics.segment_analytics_object from gpx_analytics.segment_analytics
#from gpx_analytics.segment_analytics import  segment_analytics_object


def do_Analysis():

    file_name=None
    my_segment_1 = gpx_analytics.segment_analytics.segment_analytics_object.segment_analytics_object()
    my_segment_2 = gpx_analytics.segment_analytics.segment_analytics_object.segment_analytics_object()

    ##  
    if len(sys.argv) != 3:
        print("ERROR: argument(s) missing.\n USE:  v00.py  <FILE_1>  <FILE_2>")
        return 


    if len(sys.argv)==3  and 'gpx' in sys.argv[1]:
        file_name = sys.argv[1]
        my_segment_1.load_gpx(file_name)
    elif len(sys.argv)==3  and 'csv' in sys.argv[1]:
        file_name = sys.argv[1]
        my_segment_1.load_csv(file_name)
    else:
        print("No valid file specified")
        return




    if len(sys.argv)==3  and 'gpx' in sys.argv[2]:
        file_name = sys.argv[2]
        my_segment_2.load_gpx(file_name)
    elif len(sys.argv)==3  and 'csv' in sys.argv[2]:
        file_name = sys.argv[2]
        my_segment_2.load_csv(file_name)
    else:
        print("No valid file specified")
        return


    
    new_list = gpx_analytics.algorithms.distances.join(my_segment_1,my_segment_2)
    my_segment_3 = gpx_analytics.segment_analytics.segment_analytics_object.segment_analytics_object()
    my_segment_3.load_from_list(new_list)


    #for item in new_list:
    #    print(item)

    
    my_segment_3.analyses("RAW_VELOCITY|FILTERED_VELOCITY|FILTERED_PACE")





    return 


if __name__ == "__main__":
    do_Analysis()

