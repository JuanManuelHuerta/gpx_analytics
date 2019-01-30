
import sys
import operator
import gpx_analytics
import gpx_analytics.segment_analytics
import gpx_analytics.segment_analytics.segment_analytics_object
from math import radians, cos, sin, asin, sqrt



def my_haversine(lon1, lat1, lon2, lat2):
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


def super_basic_interpolation(p1,p2):
    result = ((p1[0]+p2[0])/2.0,(p1[1]+p2[1])/2.0,None)
    return result


def distance_with_shift(s_1,s_2,shift_1):
    d= 0.0
    d_1={}
    d_2={}

    for point in s_1.X:
        d_1[point[0]]=point[1]

    for point in s_2.X:
        d_2[point[0]]=point[1]

    d=0.0
    n=0.0
    for point in d_1.items():
        t = point[0] + shift_1
        if t in d_2:
            d+=my_haversine(point[1][0],point[1][1],d_2[t][0], d_2[t][1])
            n+=1.0

    return shift_1, d

def  join(my_segment_1,my_segment_2):

    min_d = None
    min_i = None
    for i in range(30):
        this_i, this_d =  distance_with_shift(my_segment_1,my_segment_2,i-15.0)
        if min_d is None:
            min_i = this_i
            min_d = this_d
        if this_d < min_d:
            min_i = this_i
            min_d = this_d
            
    total_dict={}
    just_left=0
    just_right=0
    both=0
    for point in my_segment_1.X:
        total_dict[point[0]]=[point[1],None]
    for point in my_segment_2.X:
        t=point[0]-min_i
        if not t in total_dict:
            total_dict[t]=[None,None]
        total_dict[t][1]=point[1]
        

    #for point in sorted(total_dict.items(),key=operator.itemgetter(0)):
    #    if point[1][0] is None:
    #        just_right+=1
    #    if point[1][1] is None:
    #        just_left+=1
    #    if point[1][0] is not None and point[1][1] is not None:
    #        both+=1
    #    print(point)
            
    #print(just_left, just_right, both)


    for key in total_dict:
        if total_dict[key][0] is None:
            total_dict[key]=(total_dict[key][1][0],total_dict[key][1][1],None)
        elif total_dict[key][1]is None:
            total_dict[key]=(total_dict[key][0][0],total_dict[key][0][1],None)
        else:
            total_dict[key]=super_basic_interpolation(total_dict[key][0],total_dict[key][1])



    return [x for x in  sorted(total_dict.items(),key=operator.itemgetter(0))]
