#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

from ..utils import *
from ..erb import *
from ..measurement import *

class Technique(object):
	
	def __init__(self, erb_list):
		self.erb_list = erb_list
		self.name = ""
		self.param_dict = {}

	def SetName(self, name):
		self.name = name

	def SetTrainerParams(self, param_dict):
		self.param_dict = param_dict

	def SetMatcherParams(self, param_dict):
		self.param_dict = param_dict

	def Save(self, filename):
		raise NotImplementedError

	def Load(self, filename):
		raise NotImplementedError

	def Train(self, train_list, grid_points_filename):
		raise NotImplementedError

	#Returns predicted latitude and longitude
	def TestSample(self, test_sample):
		raise NotImplementedError

	#Test a list of samples and calculates error measures
	def TestList(self, test_list):
		errors = []
		avg_error = 0.0
		rms_error = 0.0
		
		#Calculate AVG and RMS errors
		for t in test_list:
			pred_lat, pred_lon = self.TestSample(t)
			error = DistanceInKm(t.lat, t.lon, pred_lat, pred_lon)
			errors.append(error)
			#print "\tSample Error: {} km".format(error)
			avg_error = avg_error + error
			rms_error = rms_error + error**2

		avg_error = avg_error / float(len(test_list))
		rms_error = math.sqrt(rms_error / float(len(test_list)))

		#Calculate standart deviation and variance of errors
		deviation = 0.0
		variance = 0.0
		for e in errors:
			variance = variance + (e-avg_error)**2
		variance = variance / float(len(test_list))
		deviation = math.sqrt(variance*1000)/1000.0

		#Return error metrics in meters
		return (avg_error, rms_error, deviation, variance)