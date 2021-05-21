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
from sklearn.neural_network import MLPRegressor

#---------------------------
#MLP Grid Trainer
#Dictionary Params
	#param_activation_function: ['identity', 'logistic', 'tanh', 'relu']
	#param_learning_rate: ['constant', 'invscaling', 'adaptive']
	#param_hidden_layer_size: integer
	#normalizer_file: string 'path/file'
class MLPGridTrainer(AbstractGridTrainer):

	def __init__(self, param_dict):
		AbstractGridTrainer.__init__(self, param_dict)
		self.activation_function = self.param_dict['param_activation_function']
		self.hidden_layer_size = self.param_dict['param_hidden_layer_size']
		self.learning_rate = self.param_dict['param_learning_rate']
		self.normalizer_file = self.param_dict['normalizer_file']

		#This trainer uses a model for each ERB
		self.models = []

	def TrainModel(self, erb_list, train_list):
		print "\tTraining MLP models..."

		#Loads a normalizer
		self.normalizer = Normalizer()
		self.normalizer.Load(self.normalizer_file)

		#Trains a model for each ERB
		for i in range(len(erb_list)):
			
			#Initialize Model
			model = MLPRegressor(max_iter=200, solver='adam', alpha=0.0001, 
				activation=self.activation_function,
				hidden_layer_sizes=self.hidden_layer_size,
				learning_rate=self.learning_rate
			)

			#Create sample_list is in the format [[x11, x12, ..., x1n, y1], [x21, x22, ..., x2n, y2], ...]
			sample_list = []
			for m in train_list:

				#Normalizes samples
				m = self.normalizer.NormalizeSample(m)

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
		#Normalizes sample
		cell = self.normalizer.NormalizeSample(cell)

		atributes = [cell.lat, cell.lon]
		X = numpy.array(atributes)

		for i in range(len(erb_list)):
			with warnings.catch_warnings():
				warnings.simplefilter('ignore', DeprecationWarning)
				cell.rssi[i] = self.models[i].predict(X)[0]

		#Denormalizes sample
		cell = self.normalizer.DenormalizeSample(cell)

		return cell