#!/usr/bin/python
# -*- coding: utf-8 -*-

class ERB(object):

	def __init__(self):
		self.nr = None	#Id from ERB (string)	
		self.name = None #ERB name
		self.lat = None	#ERB latitude coordinate
		self.lon = None	#ERB longitude coordinate
		self.band = None #Band used by the ERB (string ex: "GSM1800")
		self.bcch = None #Controll Channel used by the ERB (integer)
		self.eirp = None #Isotropically radiated power

	@classmethod
	def Read(cls, str_erb):
		instance = cls()
		instance.ReadFromString(str_erb)
		return instance

	def ReadFromString(self, str_erb):
		if(str_erb == '' or str_erb == '\n'):
			return

		data = str_erb.split(",")
		self.nr 	= data[0]
		self.name 	= data[1]
		self.lat 	= float(data[2])
		self.lon 	= float(data[3])
		self.band 	= data[4]
		self.bcch 	= int(data[5])
		self.eirp 	= float(data[6])

def ReadERBsFromFile(filename):
	erb_list = []
	f = open(filename, "r")

	if(not f.closed):
		for line in f:
			erb_obj = ERB.Read(line)
			erb_list.append(erb_obj)
		f.close()
	else:
		print ("Error. File " + filename + "could not be opened.");

	return erb_list