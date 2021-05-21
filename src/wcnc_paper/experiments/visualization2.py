#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import json
import numpy as np
import matplotlib as mpl
mpl.rc('font', family='Times New Roman') 
import matplotlib.pyplot as plt

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.utils import *

def include_point(grid_point, measurement=None):
	min_lat = -8.074#-8.077576
	max_lat = -8.061#-8.059338
	min_lon = -34.90#-34.90683
	max_lon = -34.885#-34.88506

	if(grid_point != None):
		lat = float(grid_point["lat"])
		lon = float(grid_point["lng"])

	if(measurement != None):
		lat = measurement.lat
		lon = measurement.lon

	if(lat < min_lat or lat > max_lat or lon < min_lon or lon > max_lon):
		return False

	return True


if __name__ == "__main__":

	#-----------------------------------------------------
	#DETERMINE POINTS TO BE PLOTTED
	#-----------------------------------------------------
	output_filename = "doc/visualization/plot.png"
	erb_list = ReadERBsFromFile('data/erbs/erbs_big.csv')
	
	lat_list = []
	lon_list = []
	color_list = []
	grid_points_filename = "data/grid_points/gpb3_roadmap_grid_20m.json"#"data/grid_points/roadmap_big_50m.json"
	with open(grid_points_filename) as data_file:    
		data = json.load(data_file)
		for point in data:
			if(include_point(point)):
				lat_list.append(float(point["lat"]))
				lon_list.append(float(point["lng"]))
				color_list.append((1.0, 0.0, 0.0))

	lat_list2 = []
	lon_list2 = []
	color_list2 = []
	grid_points_filename2 = "data/grid_points/squaremap_big_20m.json"
	with open(grid_points_filename2) as data_file:    
		data = json.load(data_file)
		for point in data:
			if(include_point(point)):
				lat_list2.append(float(point["lat"]))
				lon_list2.append(float(point["lng"]))
				color_list2.append((0.0, 1.0, 0.0))

	lat_list3 = []
	lon_list3 = []
	color_list3 = []
	sample_list = ReadMeasurementsFromFile(erb_list, 'data/samples/full_big.csv')
	for m in sample_list:
		if(include_point(None, m)):
		 	lat_list3.append(m.lat)
		 	lon_list3.append(m.lon)
		 	color_list3.append((0.0, 0.0, 1.0))

	#-----------------------------------------------------
	#DETERMINE ERB PARAMETERS
	#-----------------------------------------------------
	erb_lats = []
	erb_lons = []
	erb_marker = (3,1)
	erb_color = (0.0, 0.0, 0.0)
	erb_size = 600
	for erb in erb_list:
		erb_lats.append(erb.lat)
		erb_lons.append(erb.lon)

	#-----------------------------------------------------
	#PLOT DATA SAMPLES
	#-----------------------------------------------------
	title = ""
	x_title = "Longitude"
	y_title = "Latitude"
	x_axis = lon_list
	y_axis = lat_list
	color_list = color_list

	min_x = min(min(x_axis), min(lon_list2))#min(x_axis)
	max_x = max(max(x_axis), max(lon_list2))#max(x_axis)
	min_y = min(min(y_axis), min(lat_list2))#min(y_axis)
	max_y = max(max(y_axis), max(lat_list2))#max(y_axis)

	print "lat:[{} - {}], lon:[{} - {}]".format(min_y, max_y, min_x, max_x)

	border = 0.001
	#min_x = min_x-border
	#max_x = max_x+border
	#min_y = min_y-border
	#max_y = max_y+border

	fig = plt.figure(1, figsize = (16,9))
	ax = fig.add_subplot(111);
	ax.set_xlim([min_x, max_x])
	ax.set_ylim([min_y, max_y])
	ax.set_xlabel(x_title, fontsize=26);
	ax.set_ylabel(y_title, fontsize=26);
	ax.grid(False);
	ax.tick_params(axis='x', labelsize=22)
	ax.tick_params(axis='y', labelsize=22)
	ax.get_xaxis().get_major_formatter().set_useOffset(False)
	ax.get_yaxis().get_major_formatter().set_useOffset(False)
	plt.suptitle(title)

	plt.scatter(lon_list2, lat_list2, color=color_list2, s=12, marker='s', label="REGULAR GRID")
	plt.scatter(x_axis, y_axis, color=color_list, s=10, marker='o', label="IRREGULAR GRID")
	plt.scatter(lon_list3, lat_list3, color=color_list3, s=20, marker='o', label="MEASUREMENTS")
	
	ax.legend(prop={'size': 18})

	#plt.scatter(erb_lons, erb_lats, color=erb_color, s=erb_size, marker=erb_marker)
	plt.savefig(output_filename)
	plt.show()