#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.utils import *

if __name__ == "__main__":

	#-----------------------------------------------------
	#READ PROGRAM PARAMETERS
	#-----------------------------------------------------
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--sample_file", type=str, help="choose sample file", default='data/samples/full.csv')
	parser.add_argument("-e", "--erb", type=int, help="choose erb", default=0)
	args = parser.parse_args()

	#Read training dataset from csv file
	erb_list = ReadERBsFromFile('data/erbs/erbs.csv')
	sample_list = ReadMeasurementsFromFile(erb_list, args.sample_file)

	#-----------------------------------------------------
	#DETERMINE COLOR FOR EACH SAMPLE BASED ON RSSI
	#-----------------------------------------------------
	lat_list = [sample.lat for sample in sample_list]
	lon_list = [sample.lon for sample in sample_list]
	rssi_list = [sample.rssi[args.erb] for sample in sample_list]

	min_rssi = min(rssi_list)
	max_rssi = max(rssi_list)

	color_list = []
	for rssi in rssi_list:
		dif = ((rssi-min_rssi)/(max_rssi-min_rssi))
		r = dif*255
		g = (1-dif)*255
		b = 0
		color = (r*(1/255.0), g*(1/255.0), b*(1/255.0))
		color_list.append(color)
	print "MIN RSSI: {}".format(min_rssi)
	print "MAX RSSI: {}".format(max_rssi) 
	#-----------------------------------------------------
	#DETERMINE ERB PARAMETERS
	#-----------------------------------------------------
	erb_lat = erb_list[args.erb].lat
	erb_lon = erb_list[args.erb].lon
	erb_marker = (3,1)
	erb_color = (0.0, 0.0, 0.0)
	erb_size = 200

	#-----------------------------------------------------
	#PLOT DATA SAMPLES
	#-----------------------------------------------------
	title = ""
	x_title = "Longitude"
	y_title = "Latitude"
	x_axis = lon_list
	y_axis = lat_list
	color_list = color_list
	filename = "doc/visualization/plot.png"

	fig = plt.figure(1, figsize = (16,9))
	ax = fig.add_subplot(111);	
	ax.set_xlim([min(x_axis), max(x_axis)])
	ax.set_ylim([min(y_axis), max(y_axis)])
	ax.set_xlabel(x_title);
	ax.set_ylabel(y_title);
	ax.grid(False);
	plt.suptitle(title)
	plt.scatter(x_axis, y_axis, color=color_list, s=30)
	plt.scatter([erb_lon], [erb_lat], color=erb_color, s=erb_size, marker=erb_marker)
	plt.savefig(filename)
	plt.show()