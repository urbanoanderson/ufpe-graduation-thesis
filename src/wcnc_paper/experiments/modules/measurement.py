#!/usr/bin/python
# -*- coding: utf-8 -*-

#Custom files
from utils import *
from erb import *

#Standart lib utils
import numpy
import math

class Measurement(object):

	#Constructor
	def __init__(self, num_erbs):
		self.num_erbs = num_erbs			#Number of erbs used
		self.rssi = [None] * num_erbs 		#Array with RSS values for each ERB
		self.pathloss = [None] * num_erbs 	#Array with PATHLOSS values for each ERB		
		self.ta = [None] * num_erbs 		#Array with TA values for each ERB				
		self.lat = None						#Real latitude of the measurement point
		self.lon = None						#Real longitude of the measurement point

	@classmethod
	def Create(cls, num_erbs, lat, lon):
		m = cls(num_erbs)
		m.lat = lat
		m.lon = lon
		m.rssi = [0.0] * num_erbs
		m.ta = [0] * num_erbs
		return m

	#String representation
	def __str__(self):
		str_rep = ''
		str_rep += str(self.lat) + ','
		str_rep += str(self.lon) + ','		
		
		for i in range(len(self.rssi)-1):
			str_rep += str(self.rssi[i]) + ','
		str_rep += str(self.rssi[len(self.rssi)-1])	

		#for i in range(len(self.rssi)):
		#	str_rep += str(self.rssi[i]) + ','
		#for i in range(len(self.ta)-1):
		#	str_rep += str(self.ta[i]) + ','
		#str_rep += str(self.ta[len(self.ta)-1])	

		return str_rep

	#Readable string representation
	def ReadableStrRepr(self):
		str_rep = ''

		if self.lat is not None:
			str_rep += 'LAT: ' + str(self.lat) + ' '
		if self.lon is not None:
			str_rep += 'LON: ' + str(self.lon)
		for i in range(len(self.rssi)):
			if self.rssi[i] is not None:
				str_rep += 'RSS' + str(i+1) + ': ' + str(self.rssi[i]) + ' '
		for i in range(len(self.pathloss)):
			if self.pathloss[i] is not None:
				str_rep += 'PATHLOSS' + str(i+1) + ': ' + str(self.pathloss[i]) + ' '
		for i in range(len(self.ta)):
			if self.ta[i] is not None:
				str_rep += 'TA' + str(i+1) + ': ' + str(self.ta[i]) + ' '

		return str_rep

	def InitFromString(self, str_measurement, erb_list):
		data = str_measurement.split(",")
		self.lat 	= float(data[0])
		self.lon 	= float(data[1])

		for i in range(len(erb_list)):
			self.rssi[i] = float(data[2+i])

		self.CalcPathlossValues(erb_list)
		self.CalcTAValues(erb_list)

	def CalcPathlossValues(self, erb_list):
		for i in range(len(erb_list)):
			self.pathloss[i] = erb_list[i].eirp - self.rssi[i]

	def CalcTAValues(self, erb_list):
		for i in range(len(erb_list)):
			dist = int(DistanceInKm(self.lat, self.lon, erb_list[i].lat, erb_list[i].lon)*1000.0)
			self.ta[i] = (dist / 550)

#---------------------------------------------------------

def ReadMeasurementsFromFile(erb_list, filename):
	measurement_list = []
	f = open(filename, "r")

	if(not f.closed):
		f.readline()	#ignore first line
		for line in f:
			measurement_obj = Measurement(len(erb_list))
			measurement_obj.InitFromString(line, erb_list)
			measurement_list.append(measurement_obj)
		f.close()
	else:
		print ("Error. File " + filename + "could not be opened.");

	return measurement_list

def WriteMeasurementsToFile(measurement_list, filename):
	f = open(filename, "w")
	if(not f.closed):
		f.write('lat,lon,RSSI[]' + '\n')
		for measurement in measurement_list:
			f.write(str(measurement) + '\n')
	f.close()