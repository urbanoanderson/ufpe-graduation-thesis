#!/usr/bin/python
# -*- coding: utf-8 -*-

from modules.erb import *
from modules.measurement import *

import math

if __name__ == "__main__":

	#Read ERB database
	erb_list = ReadERBsFromFile('data/erbs.csv')
	measurement_list = ReadMeasurementsFromFile(erb_list, 'data/train_samples/train_full.csv')
	grid_list = ReadMeasurementsFromFile(erb_list, 'data/technique_data/fp_math/grid_free_space.csv')

	super_list = measurement_list + grid_list

	#Find min and max rss, pathloss, latitude and longitude
	min_lat = 99999999.9
	min_lon = 99999999.9
	max_lat = -99999999.9
	max_lon = -99999999.9
	min_rss = [99999999.9] * len(erb_list)
	min_pathloss = [99999999.9] * len(erb_list)
	max_rss = [-99999999.9] * len(erb_list)
	max_pathloss = [-99999999.9] * len(erb_list)

	for m in super_list:
		min_lat = min(min_lat, m.lat)
		min_lon = min(min_lon, m.lon)
		max_lat = max(max_lat, m.lat)
		max_lon = max(max_lon, m.lon)
		for i in range(len(erb_list)):
			min_rss[i] = min(min_rss[i], m.rss[i])
			min_pathloss[i] = min(min_pathloss[i], m.pathloss[i])
			max_rss[i] = max(max_rss[i], m.rss[i])
			max_pathloss[i] = max(max_pathloss[i], m.pathloss[i])

	#Print results
	print "Lat: {} | {}".format(min_lat, max_lat)
	print "Lon: {} | {}".format(min_lon, max_lon)
	print "RSS: {} | {}".format(min_rss, max_rss)
	print "PATHLOSS: {} | {}".format(min_pathloss, max_pathloss)