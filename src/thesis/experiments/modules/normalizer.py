#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import sys
import math
import numpy

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *

class Normalizer(object):

	def __init__(self, sample_list=[]):

		if sample_list != []:
			self.BIG_VALUE = 99999999999.9
			self.SMALL_VALUE = -99999999999.9

			self.min_lat = self.BIG_VALUE
			self.max_lat = self.SMALL_VALUE
			self.min_lon = self.BIG_VALUE
			self.max_lon = self.SMALL_VALUE 
			self.min_rssi = [self.BIG_VALUE] * len(sample_list[0].rssi)
			self.max_rssi = [self.SMALL_VALUE] * len(sample_list[0].rssi)

			for sample in sample_list:
				self.min_lat = min(self.min_lat, sample.lat)
				self.max_lat = max(self.max_lat, sample.lat)
				self.min_lon = min(self.min_lon, sample.lon)
				self.max_lon = max(self.max_lon, sample.lon)

				for i in range(len(sample_list[0].rssi)):
					self.min_rssi[i] = min(self.min_rssi[i], sample.rssi[i])
					self.max_rssi[i] = max(self.max_rssi[i], sample.rssi[i])

	def Norm(self, value, min_value, max_value):
		return ((value - min_value) / float(max_value - min_value))

	def Denorm(self, norm_value, min_value, max_value):
		return norm_value*(max_value-min_value) + min_value

	def NormalizeSample(self, sample):
		normalized = Measurement.Create(len(sample.rssi), 0.0, 0.0)
		normalized.lat = self.Norm(sample.lat, self.min_lat, self.max_lat)
		normalized.lon = self.Norm(sample.lon, self.min_lon, self.max_lon)
		for i in range(len(sample.rssi)):
			normalized.rssi[i] = self.Norm(sample.rssi[i], self.min_rssi[i], self.max_rssi[i])
		
		return normalized

	def DenormalizeSample(self, norm_sample):
		denormalized = Measurement.Create(len(norm_sample.rssi), 0.0, 0.0)
		denormalized.lat = self.Denorm(norm_sample.lat, self.min_lat, self.max_lat)
		denormalized.lon = self.Denorm(norm_sample.lon, self.min_lon, self.max_lon)
		for i in range(len(norm_sample.rssi)):
			denormalized.rssi[i] = self.Norm(norm_sample.rssi[i], self.min_rssi[i], self.max_rssi[i])
		
		return denormalized

	def NormalizeSampleList(self, sample_list):
		norm_list = []
		for sample in sample_list:
			norm_list.append(self.NormalizeSample(sample))
		return norm_list

	def DenormalizeSampleList(self, norm_sample_list):
		sample_list = []
		for norm_sample in norm_sample_list:
			sample_list.append(self.DenormalizeSample(norm_sample))
		return sample_list

	def Save(self, filename):
		f = open(filename, "w")
		if(not f.closed):
			f.write("{} {}\n".format(self.min_lat, self.max_lat))
			f.write("{} {}\n".format(self.min_lon, self.max_lon))
			f.write("{}\n".format(len(self.min_rssi)))
			for i in range(len(self.min_rssi)):
				f.write("{} {}\n".format(self.min_rssi[i], self.max_rssi[i]))
		f.close()

	def Load(self, filename):
		f = open(filename, "r")

		if(not f.closed):
			a, b = f.readline().split()
			self.min_lat = float(a)
			self.max_lat = float(b)
			a, b = f.readline().split()
			self.min_lon = float(a)
			self.max_lon = float(b)
			num_erbs = int(f.readline().strip())
			self.min_rssi = [0.0] * num_erbs
			self.max_rssi = [0.0] * num_erbs
			for i in range(num_erbs):
				a, b = f.readline().split()
				self.min_rssi[i] = float(a)
				self.max_rssi[i] = float(b)
			f.close()
		else:
			print ("Normalizer Error. File " + filename + "could not be opened.");