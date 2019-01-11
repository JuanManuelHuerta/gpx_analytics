# gpx_analytics

Spectral Analysis of GPS signals: GPX files downloaded from Strava.


to run:

python v00.py <gpx.file_to_be_proccessed>



Dependencies: numpy, haversine, etc etc. See all imports.


See the Wiki for images:
https://github.com/JuanManuelHuerta/gpx_analytics/wiki


Backlog:

	1. The GPS raw signal already has a Filter, it seems that the filter of v00 is most probably correcting "decimal truncation" noise in the time signal. Investigate.
	2. Integrate elevation into the calculation...
	3. How about GAP, etc?
	4. Once signal is relatively cleaned: Perform Spectral Analysis (which was the original idea!)
	5. How about segments? what if there wasa "break" during activity? Also: GPS seems to not be spaced equally in time. Need to extrapolate because current spectral analysis assumes equally spaced sampling
	6. Implement Short Term fourier i.e., periodogram/spectrogram
	7. How about DTW between 2 instances of the same segment? [3]
	
	[1] Wiener-Khinchin https://en.wikipedia.org/wiki/Wiener%E2%80%93Khinchin_theorem
	[2] Kalman https://en.wikipedia.org/wiki/Kalman_filter
	[3] DTW https://en.wikipedia.org/wiki/Dynamic_time_warping
	

