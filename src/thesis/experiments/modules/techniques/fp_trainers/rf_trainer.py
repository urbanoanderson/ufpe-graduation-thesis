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
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

#---------------------------
#Random Forest Grid Trainer
#Dictionary Params
	#param_n_estimators: integer
class RFGridTrainer(AbstractGridTrainer):

	def __init__(self, param_dict):
		AbstractGridTrainer.__init__(self, param_dict)
		self.n_estimators = self.param_dict['param_n_estimators']

		#This trainer uses one model for each ERB
		self.models = []

	def TrainModel(self, erb_list, train_list):
		print "\tTraining Random Forest models..."

		#Trains a model for each ERB
		for i in range(len(erb_list)):
			
			#Initialize MLP
			model = RandomForestRegressor(n_estimators=self.n_estimators, random_state=0)

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
		X = numpy.array(atributes)

		for i in range(len(erb_list)):
			with warnings.catch_warnings():
				warnings.simplefilter('ignore', DeprecationWarning)
				cell.rssi[i] = self.models[i].predict(X)[0]

		return cell