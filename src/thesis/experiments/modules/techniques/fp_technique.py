#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from ..utils import *
from ..erb import *
from ..timer import *
from ..measurement import *
from ..normalizer import *

from technique import *

from fp_trainers.trainer import *
from fp_trainers.knn_trainer import *
from fp_trainers.mlp_trainer import *
from fp_trainers.svm_trainer import *
from fp_trainers.rf_trainer import *

#---------------------------------------------------------------------
#FINGERPRINTING TECHNIQUE
#---------------------------------------------------------------------

#PARAMS:
#'grid_trainer': 'knn', 'ml'
#'grid_filename': 'path/file'  (output grid filename)
#'grid_points_filename': 'path/file'   (input grid points)
class FingerprintingTechnique(Technique):

	def __init__(self, erb_list):
		Technique.__init__(self, erb_list)
		self.name = "Fingerprinting"
		self.grid_list = []
		self.grid_trainer = None

	def SetParams(self, param_dict):
		Technique.SetParams(self, param_dict)

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

	def Save(self):
		WriteMeasurementsToFile(self.grid_list, self.param_dict['grid_filename'])

	def Load(self):
		self.grid_list = ReadMeasurementsFromFile(self.erb_list, self.param_dict['grid_filename'])

	def Train(self, train_list):
		#Read grid points from json
		with open(self.param_dict['grid_points_filename']) as data_file:    
			data = json.load(data_file)
			for point in data:
				self.grid_list.append(Measurement.Create(len(self.erb_list), float(point["lat"]), float(point["lng"])))

		#Use trainer to estimate rssi of grid
		self.grid_trainer.TrainGrid(self.grid_list, self.erb_list, train_list)

	def TestSample(self, test_sample):
		chosen_cell = self.grid_list[0]

		min_dist = 99999999.9
		for cell in self.grid_list:
			dist = SquareDistance(test_sample.rssi, cell.rssi)

			if(dist < min_dist):
				min_dist = dist
				chosen_cell = cell

		return chosen_cell.lat, chosen_cell.lon