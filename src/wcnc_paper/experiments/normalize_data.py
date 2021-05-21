#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.utils import *

if __name__ == "__main__":

	#-----------------------------------------------------
	#READ INPUT FILES
	#-----------------------------------------------------
	erb_list = ReadERBsFromFile('data/erbs/erbs1.csv')
	sample_list = ReadMeasurementsFromFile(erb_list, 'data/samples/full1.csv')
	output_file = 'data/samples/full1_norm.csv'

	#-----------------------------------------------------
	#DETERMINE MIN, MAX AND AVERAGE COORDINATES AND RSSI FOR EACH ERB
	#-----------------------------------------------------
	BIG_NUMBER = 	9999999.9
	SMALL_NUMBER = -9999999.9
	lat_values = [BIG_NUMBER, SMALL_NUMBER, 0.0] #[MIN,MAX,AVG]
	lon_values = [BIG_NUMBER, SMALL_NUMBER, 0.0] #[MIN,MAX,AVG]
	rssi_values = []
	for i in range(len(erb_list)):
		rssi_values.append([BIG_NUMBER, SMALL_NUMBER, 0.0])

	for m in sample_list:
		lat_values[0] = min(lat_values[0], m.lat)
		lat_values[1] = max(lat_values[1], m.lat)
		lat_values[2] += m.lat
		lon_values[0] = min(lon_values[0], m.lon)
		lon_values[1] = max(lon_values[1], m.lon)
		lon_values[2] += m.lon

		for i in range(len(erb_list)):
			rssi_values[i][0] = min(rssi_values[i][0], m.rssi[i])
			rssi_values[i][1] = max(rssi_values[i][1], m.rssi[i])
			rssi_values[i][2] += m.rssi[i]

	lat_values[2] /= float(len(sample_list))
	lon_values[2] /= float(len(sample_list))
	for i in range(len(erb_list)):
		rssi_values[i][2] /= float(len(sample_list))

	print lat_values
	print lon_values
	print rssi_values

	#-----------------------------------------------------
	#NORMALIZE EACH MEASUREMENT
	#-----------------------------------------------------
	for m in sample_list:
		for i in range(len(erb_list)):
			m.rssi[i] /= rssi_values[i][2]
	
	#-----------------------------------------------------
	#SAVE OUTPUT FILE
	#-----------------------------------------------------
	WriteMeasurementsToFile(sample_list, output_file)