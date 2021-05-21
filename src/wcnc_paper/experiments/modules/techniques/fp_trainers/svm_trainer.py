#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import json
import random
import numpy
import warnings

from ...utils import *
from ...erb import *
from ...timer import *
from ...measurement import *

from trainer import *

from sklearn.exceptions import ConvergenceWarning
from sklearn.svm import SVR

#---------------------------
#SVM Grid Trainer
#Dictionary Params
	#trainer_param_kernel: ['rbf', 'linear', 'sigmoid', 'poly']
	#trainer_param_c: float
	#trainer_param_e: float between 0 and 1
class SVMGridTrainer(AbstractGridTrainer):

	def __init__(self, param_dict):
		AbstractGridTrainer.__init__(self, param_dict)
		self.kernel = self.param_dict['trainer_param_kernel']
		self.C = self.param_dict['trainer_param_c']
		self.e = self.param_dict['trainer_param_e']

		#This trainer uses one model for each ERB
		self.models = []

	def TrainModel(self, erb_list, train_list):
		print "\tTraining SVM models..."

		#Trains a model for each ERB
		for i in range(len(erb_list)):
			
			if type(self.C) is list:
				param_C = self.C[i]
			else:
				param_C = self.C

			#Initialize MLP
			model = SVR(C=param_C, epsilon=self.e, kernel=self.kernel)

			#Create sample_list is in the format [[x11, x12, ..., x1n, y1], [x21, x22, ..., x2n, y2], ...]
			sample_list = []
			for m in train_list:
				parameter_list = [m.lat, m.lon, m.rssi[i]]
				sample_list.append(parameter_list)

			#Generate X and Y arrays to train
			X_train = numpy.array([[sublist[j] for j in range(len(sublist)-1)] for sublist in sample_list])
			Y_train = numpy.array([sublist[len(sublist)-1] for sublist in sample_list])

			#Train model
			with warnings.catch_warnings():
				warnings.simplefilter('ignore', ConvergenceWarning)
				model.fit(X_train, Y_train)

			#Stores the ERB model
			self.models.append(model)

	def PredictCellRSSI(self, cell, erb_list, train_list):
		atributes = [cell.lat, cell.lon]
		X = numpy.array(atributes).reshape((1, -1))

		for i in range(len(erb_list)):
			cell.rssi[i] = self.models[i].predict(X)[0]

		cell.CalcPathlossValues(erb_list)
		cell.CalcTAValues(erb_list)
			
		return cell