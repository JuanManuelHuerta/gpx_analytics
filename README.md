# gpx_analytics
Spectral Analysis of GPS signals


to run:

python v00.py <gpx.file_to_be_proccessed>



Dependencies: numpy, haversine, etc et.


See the Wiki for images:
https://github.com/JuanManuelHuerta/gpx_analytics/wiki


Backlog:

	1. The GPS raw signal already has a Filter, it seems that the filter of v00 is most probably correcting "decimal truncation" noise in the time signal. Investigate.
	2. Integrate elevation into the calculation...
	3. How about GAP, etc?
	4. Once signal is relatively cleaned: Perform Spectral Analysis (which was the original idea!)
	
	
	[1] Wiener-Khinchin https://en.wikipedia.org/wiki/Wiener%E2%80%93Khinchin_theorem
	[2] Kalman https://en.wikipedia.org/wiki/Kalman_filter

