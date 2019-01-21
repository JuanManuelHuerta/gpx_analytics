# gpx_analytics

License: MIT

This code is intended to perform the analysis of Geospatial GPS signals for outdoor movement tracking.
Formats supported: GPX, and CSV.

# SIMPLE CALCULATIONS/PLOTS:

- RAW_VELOCITY         :  Calculated from the Lat-Long measurements

- FILTERED_PACE        :  Calculated pace from the Filtered Velocity

- ELEVATION            :  Elevation curve provided by measurements

- HEART_RATE_CURVE     :  From Measurements

- HR_PACE_SCATTER      : Scatter plot of heart rate and pace

# ALGORITHMS/TRANSFORMATIONS:

- FILTERED_VELOCITY    :  Same as raw velocity, but with an LPF smoothing

- LOG_POWER_SPECTRUM   :  Full file LPS, reveals periodicity (and hence measurment issues)

- SPECTROGRAM          :  Shows temporal view of spectral components of velocity: low changing, medium changing, high changing

- GAP                   : Experimental calculation of Grade Adjusted Pace




# To run:

python3 v00.py <gpx.file_to_be_proccessed>  "<PIPE_DELIMITED_ANALYSIS_STRING>"

Please choose up to 5 options.

Two windows will open: one with the calculated versus device measurement, and the other with the specified analysis.

# Example
python3 v00.py my_file.csv  "RAW_VELOCITY|FILTERED_PACE|HR_PACE"

Module and package dependencies: basic Python packages (math, operator, numpy, seaborn, pandas etc.) See all import statements.

Runs on Python 3.


See the Wiki in the repo for images:

https://github.com/JuanManuelHuerta/gpx_analytics/wiki


