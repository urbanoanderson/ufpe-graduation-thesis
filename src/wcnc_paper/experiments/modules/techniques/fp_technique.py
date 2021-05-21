#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from ..utils import *
from ..erb import *
from ..timer import *
from ..measurement import *

from technique import *

from fp_trainers.trainer import *
from fp_trainers.knn_trainer import *
from fp_trainers.mlp_trainer import *
from fp_trainers.svm_trainer import *
from fp_trainers.rf_trainer import *

from fp_matchers.matcher import *
from fp_matchers.knn_matcher import *
from fp_matchers.distance_matcher import *

#---------------------------------------------------------------------
#FINGERPRINTING TECHNIQUE
#---------------------------------------------------------------------

#PARAMS:
#'grid_trainer': 'knn', 'ml'
#'grid_matcher': 'distance', 'knn'
class FingerprintingTechnique(Technique):

	def __init__(self, erb_list):
		Technique.__init__(self, erb_list)
		self.name = "Fingerprinting"
		self.grid_list = []
		self.grid_trainer = None
		self.grid_matcher = None

	def SetTrainerParams(self, param_dict):
		Technique.SetTrainerParams(self, param_dict)

		#Set grid trainer
		if(self.param_dict['grid_trainer'] == 'knn'):
			self.grid_trainer = KNNGridTrainer(self.param_dict)
		elif(self.param_dict['grid_trainer'] == 'mlp'):
			self.grid_trainer = MLPGridTrainer(self.param_dict)
		elif(self.param_dict['grid_trainer'] == 'svm'):
			self.grid_trainer = SVMGridTrainer(self.param_dict)
		elif(self.param_dict['grid_trainer'] == 'rf'):
			self.grid_trainer = RFGridTrainer(self.param_dict)
		else:
			print 'Fingerprinting Error: unknown grid trainer param.'
			exit()

	def SetMatcherParams(self, param_dict):
		Technique.SetMatcherParams(self, param_dict)

		#Set grid matcher
		if(self.param_dict['grid_matcher'] == 'knn'):
			self.grid_matcher = KNNGridMatcher(self.param_dict)
		elif(self.param_dict['grid_matcher'] == 'distance'):
			self.grid_matcher = DistanceGridMatcher(self.param_dict)
		else:
			print 'Fingerprinting Error: unknown grid matcher param.'
			exit()

	def Save(self, filename):
		WriteMeasurementsToFile(self.grid_list, filename)

	def Load(self, filename):
		self.grid_list = ReadMeasurementsFromFile(self.erb_list, filename)

	def Train(self, train_list, grid_points_filename):
		#Read grid points from json
		with open(grid_points_filename) as data_file:    
			data = json.load(data_file)
			for point in data:
				self.grid_list.append(Measurement.Create(len(self.erb_list), float(point["lat"]), float(point["lng"])))

			for cell in self.grid_list:
				cell.CalcTAValues(self.erb_list)

		#Use trainer to estimate rssi of grid
		self.grid_trainer.TrainGrid(self.grid_list, self.erb_list, train_list)

	def TestSample(self, test_sample):
		chosen_cell = self.grid_matcher.Match(self.grid_list, test_sample)

		return chosen_cell.lat, chosen_cell.lon

	def FilterGrid(self, test_sample):
		subsets = [[] for x in range(len(test_sample.ta)+1)]
		for cell in self.grid_list:
			points = 0
			for i in range(len(cell.ta)):
				if cell.ta[i] == test_sample.ta[i]:
					points += 1
			subsets[points].append(cell)

		for subset in reversed(subsets):
			if(len(subset) > 0):
				return subset

	def FilterGridRobson(self, test_sample):
		#WARNING: CONSIDERING A FIXED NUMBER OF 3 ERBS (CHANGE LATER)
		filtered_grid = []

		#All 3
		for cell in self.grid_list:
			if cell.ta[0] == test_sample.ta[0] and cell.ta[1] == test_sample.ta[1] and cell.ta[2] == test_sample.ta[2]:
				filtered_grid.append(cell)

		#ONLY 2
		if filtered_grid == []:
			for cell in self.grid_list:
				if cell.ta[0] == test_sample.ta[0] and cell.ta[1] == test_sample.ta[1]:
					filtered_grid.append(cell)

		if filtered_grid == []:
			for cell in self.grid_list:
				if cell.ta[0] == test_sample.ta[0] and cell.ta[2] == test_sample.ta[2]:
					filtered_grid.append(cell)

		if filtered_grid == []:
			for cell in self.grid_list:
				if cell.ta[1] == test_sample.ta[1] and cell.ta[2] == test_sample.ta[2]:
					filtered_grid.append(cell)

		#ONLY 1
		if filtered_grid == []:
			for cell in self.grid_list:
				if cell.ta[0] == test_sample.ta[0] or cell.ta[1] == test_sample.ta[1] or cell.ta[2] == test_sample.ta[2]:
					filtered_grid.append(cell)

		#NONE
		if filtered_grid == []:
			filtered_grid = self.grid_list

		return filtered_grid

	#Test a list of samples and calculates error measures
	def TestListFilter(self, test_list):
		errors = []
		avg_error = 0.0
		rms_error = 0.0
		
		#Calculate AVG and RMS errors
		for t in test_list:
			filtered_grid = self.FilterGrid(t) #self.grid_list #
			#print "\tNum of Cells in filtered grid: {}".format(len(filtered_grid))
			chosen_cell = self.grid_matcher.Match(filtered_grid, t)
			pred_lat = chosen_cell.lat
			pred_lon = chosen_cell.lon			

			error = DistanceInKm(t.lat, t.lon, pred_lat, pred_lon)
			errors.append(error)
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