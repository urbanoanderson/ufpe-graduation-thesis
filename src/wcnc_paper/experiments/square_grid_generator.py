#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.utils import *


if __name__ == "__main__":

	#Read training dataset from csv file
	erb_list = ReadERBsFromFile('data/erbs/erbs_big.csv')
	full_list = ReadMeasurementsFromFile(erb_list, 'data/samples/full_big.csv')

	#Initialize Resolution parameter
	if len(sys.argv) > 1:
		RESOLUTION = int(sys.argv[1])
	else:
		RESOLUTION = 20 #meters

	print "SQUARE GRID GENERATOR"
	print "\tResolution: {} m".format(RESOLUTION)

	#-----------------------------------------------------
	#Find diference in coordinates 
	#-----------------------------------------------------
	target_dist = RESOLUTION/1000.0 #kilometers
	diff_lat = 0.0
	diff_lon = 0.0
	inc = 0.0000001
	ref_lat = -8.077576
	ref_lon = -34.90683
	while(DistanceInKm(ref_lat, ref_lon, ref_lat+diff_lat, ref_lon) < target_dist):
		diff_lat += inc
	while(DistanceInKm(ref_lat, ref_lon, ref_lat, ref_lon+diff_lon) < target_dist):
		diff_lon += inc

	#-----------------------------------------------------
	#Find min/max coordinates
	#-----------------------------------------------------
	min_lat = 9999999.9
	max_lat = -9999999.9
	min_lon = 9999999.9
	max_lon = -9999999.9
	for i in full_list:
		if i.lat < min_lat:
			min_lat = i.lat
		if i.lat > max_lat:
			max_lat = i.lat
		if i.lon < min_lon:
			min_lon = i.lon
		if i.lon > max_lon:
			max_lon = i.lon

	#-----------------------------------------------------
	#Generate grid from point
	#-----------------------------------------------------
	ini_lat = min_lat - diff_lat
	ini_lon = min_lon - diff_lon
	dst_lat = max_lat + diff_lat
	dst_lon = max_lon + diff_lon

	cur_lat = ini_lat
	cur_lon = ini_lon
	points = []

	while cur_lat <= dst_lat:
		cur_lon = ini_lon
		while cur_lon <= dst_lon:
			points.append((cur_lat, cur_lon))
			cur_lon += diff_lon
		cur_lat += diff_lat

	print("\tNumber of generated points: {}".format(len(points)))
	print("\tLatitude Range: [{}, {}]".format(min_lat, max_lat))
	print("\tLongitude Range: [{}, {}]".format(min_lon, max_lon))	
	print("\tDistance Neighbors Row: {} km".format(DistanceInKm(points[1][0], points[1][1], points[2][0], points[2][1])))
	print("\tDistance Neighbors Col: {} km".format(DistanceInKm(ini_lat, ini_lon, ini_lat, ini_lon+diff_lon)))
	print("\tMax Distance Lat: {} km".format(DistanceInKm(points[0][0], points[0][1], points[-1][0], points[0][1])))
	print("\tMax Distance Lon: {} km".format(DistanceInKm(points[0][0], points[0][1], points[0][0], points[-1][1])))


	#-----------------------------------------------------
	#WRITE GEOGRAPHIC COORDINATES TO FILE
	#-----------------------------------------------------
	f = open("data/grid_points/squaremap_big_{}m.json".format(RESOLUTION), 'w')
	f.write("[\n")
	for i, point in enumerate(points):
		f.write("	{\n")
		f.write("		\"lat\": {},\n".format(point[0]))
		f.write("		\"lng\": {}\n".format(point[1]))
		if(i < len(points) - 1):
			f.write("	},\n")
		else:
			f.write("	}\n")
	f.write("]")
	f.close()