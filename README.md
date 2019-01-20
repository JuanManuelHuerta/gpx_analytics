# gpx_analytics

License: MIT

This code is intended to perform the analysis of Geospatial GPS signals for outdoor movement tracking.
Formats supported: GPX, and CSV.

Analyses:

RAW_VELOCITY

FILTERED_VELOCITY

FILTERED_PACE

LOG_POWER_SPECTRUM

SPECTROGRAM

HEART_RATE_CURVE

HR_PACE

HR_PACE_SCATTER

To run:
python3 v00.py <gpx.file_to_be_proccessed>  "<PIPE_DELIMITED_ANALYSIS_STRING>"

Example
python3 v00.py my_file.csv  "RAW_VELOCITY|FILTERED_PACE|HR_PACE"

Module and package dependencies: basic Python packages (math, operator, numpy, seaborn, pandas etc.) See all import statements.

Runs on Python 3.


See the Wiki in the repo for images:
https://github.com/JuanManuelHuerta/gpx_analytics/wiki


