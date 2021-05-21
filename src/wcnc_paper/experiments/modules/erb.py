#!/usr/bin/python
# -*- coding: utf-8 -*-

class ERB(object):

	def __init__(self):
		self.name = None 	#ERB name (Ex: "PE136Y")
		self.height = None 	#ERB height in meters (Ex: 41)
		self.lat = None		#ERB latitude (Ex: -8.068361)
		self.lon = None		#ERB longitude (Ex: -3.489272)
		self.elev = None	#Terrain elevation (Ex: 8)
		self.band = None	#GSM band (Ex: "GSM1800")
		self.bcch = None	#Controll Channel used by the ERB (Ex: 662)
		self.antenna = None	#Antenna model (Ex: "DX-1710-2170-65-18i-M")
		self.azimuth = None	#Angle to true north pole (Ex: 220)
		self.eirp = None	#Isotropically radiated power (Ex: 70.1)
		self.tiltEle = None	#Electric Tilt (Ex: 8)
		self.tiltMec = None	#Mechanic Tilt (Ex: 0)

	@classmethod
	def Read(cls, str_erb):
		instance = cls()
		instance.ReadFromString(str_erb)
		return instance

	def ReadFromString(self, str_erb):
		if(str_erb == '' or str_erb == '\n'):
			return

		data = str_erb.split(";")
		self.name = data[0]
		self.height = float(data[1])
		self.lat = float(data[2])
		self.lon = float(data[3])
		self.elev = int(data[4])
		self.band = data[5]
		self.bcch = int(data[6])
		self.antenna = data[7]
		self.azimuth = int(data[8])
		self.eirp = float(data[9])
		self.tiltEle = int(data[10])
		self.tiltMec = int(data[11])

def ReadERBsFromFile(filename):
	erb_list = []
	f = open(filename, "r")

	if(not f.closed):
		f.readline()	#ignore first line
		for line in f:
			erb_obj = ERB.Read(line)
			erb_list.append(erb_obj)
		f.close()
	else:
		print ("Error. File " + filename + "could not be opened.");

	return erb_list