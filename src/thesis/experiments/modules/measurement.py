#!/usr/bin/python
# -*- coding: utf-8 -*-

#Custom files
from utils import *
from erb import *

#Standart lib utils
import pyparsing
import numpy
import math

class Measurement(object):

	#Constructor
	def __init__(self, num_erbs):
		self.num_erbs = num_erbs			#Number of erbs used
		self.rssi = [None] * num_erbs 		#Array with RSS values for each ERB
		self.lat = None						#Real latitude of the measurement point
		self.lon = None						#Real longitude of the measurement point

	@classmethod
	def Create(cls, num_erbs, lat, lon):
		m = cls(num_erbs)
		m.lat = lat
		m.lon = lon
		m.rssi = [0.0] * num_erbs
		return m

	#String representation
	def __str__(self):
		str_rep = ''
		str_rep += str(self.lat) + ','
		str_rep += str(self.lon) + ','		
		for i in range(len(self.rssi)-1):
			str_rep += str(self.rssi[i]) + ','
		str_rep += str(self.rssi[len(self.rssi)-1])	

		return str_rep

	#Readable string representation
	def ReadableStrRepr(self):
		str_rep = ''

		for i in range(len(self.rssi)):
			if self.rssi[i] is not None:
				str_rep += 'RSS' + str(i+1) + ': ' + str(self.rssi[i]) + ' '
		if self.lat is not None:
			str_rep += 'LAT: ' + str(self.lat) + ' '
		if self.lon is not None:
			str_rep += 'LON: ' + str(self.lon)

		return str_rep

	def InitFromString(self, str_measurement):
		data = str_measurement.split(",")
		self.lat 	= float(data[0])
		self.lon 	= float(data[1])
		self.rssi[0] = float(data[2])
		self.rssi[1] = float(data[3])
		self.rssi[2] = float(data[4])
		self.rssi[3] = float(data[5])
		self.rssi[4] = float(data[6])
		self.rssi[5] = float(data[7])

#---------------------------------------------------------

def ReadMeasurementsFromFile(erb_list, filename):
	measurement_list = []
	f = open(filename, "r")

	if(not f.closed):
		f.readline()	#ignore first line
		for line in f:
			measurement_obj = Measurement(len(erb_list))
			measurement_obj.InitFromString(line)
			measurement_list.append(measurement_obj)
		f.close()
	else:
		print ("Error. File " + filename + "could not be opened.");

	return measurement_list

def WriteMeasurementsToFile(measurement_list, filename):
	f = open(filename, "w")
	if(not f.closed):
		f.write('lat,lon,RSSI_1,RSSI_2,RSSI_3,RSSI_4,RSSI_5,RSSI_6' + '\n')
		for measurement in measurement_list:
			f.write(str(measurement) + '\n')
	f.close()