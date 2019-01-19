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
from math import radians, cos, sin, asin, sqrt
import numpy as np
import matplotlib.pyplot as plt
import math
import gpx_analytics



def do_Analysis():
    file_name=None
    if len(sys.argv)>1 and sys.argv[1]!=None:
        file_name = sys.argv[1]
    else:
        file_name = 'data/2007129462.gpx'

    my_segment = gpx_analytics.segment()
    my_segment.load_gpx(file_name)
    my_segment.compute_velocity()
    my_segment.filter_velocity(24)
    my_segment.compute_power_spectrum()
    my_segment.make_plots()

# Plotting steps.
# Points are NOT evenly spaced, but let's ignore that fact for now
    just_X=np.array(self.just_X)

#  Log-Power Spectrum
    ps = np.log(np.abs(np.fft.fft(just_X_pace))**2)
#print ps
    plt.figure(1)

# Plot results
    plt.subplot(5,1,1)
    plt.title("Raw velocity points")
    plt.plot([x[0] for x in Xd], [x[1] for x in Xd], 'bo')

    plt.subplot(5,1,2)
    plt.title("Low-pass filtered velocity Curve")
    plt.plot([x[0] for x in Xf], [x[1] for x in Xf])
    x=[x[1] for x in Xf]
    x_p=[1.0/x[1] for x in Xf]

    plt.subplot(5,1,3)
    plt.title("Pace  Curve ")
    pc =[1.0/x[1] for x in Xf]
    plt.plot([x[0] for x in Xf],pc) 
    plt.ylim(max(pc),min(pc))

    plt.subplot(5,1,4)
    plt.title("Log Power Spectrum of the Whole Velocity Run")
    plt.plot(ps)

    plt.subplot(5,1,5)
    NFFT = 64  # the length of the windowing segments
    plt.title("Changing Log Power Spectrum (Spectrogram)")
    Pxx, freqs, bins, im = plt.specgram(x_p, NFFT=NFFT, Fs=1.0, noverlap=0 )
    plt.show()



if __name__ == "__main__":
    do_Analysis()

