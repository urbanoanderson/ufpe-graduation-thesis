#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import math
import numpy
import pickle
import warnings

#Simple Regressors
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import HuberRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import RANSACRegressor
from sklearn.linear_model import TheilSenRegressor
from sklearn.svm import SVR

#Meta-regressors
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor

#Extras
from sklearn.exceptions import ConvergenceWarning

#Custom Classes
from timer import *
from normalizer import *

#Pathloss model for 1 ERB
class LearningModel(object):

	#Default constructor
	def __init__(self, param_dict):
		self.param_dict = param_dict
		self.normalizer = Normalizer()
		self.model = None

		#Set model based on ml_algorithm parameter
		if(self.param_dict['ml_algorithm'] == 'mlp'):
			self.model = self.GetMLPRegressor()
		elif(self.param_dict['ml_algorithm'] == 'svm'):
			self.model = self.GetSVMRegressor()
		elif(self.param_dict['ml_algorithm'] == 'k_neighbors'):
			self.model = self.GetKNeighborsRegressor()
		elif(self.param_dict['ml_algorithm'] == 'random_forest'):
			self.model = RandomForestRegressor(n_estimators=200, random_state=0)	

	#Set normalizer for atributes
	def SetNormalizer(self, normalizer):
		self.normalizer = normalizer

	def Train(self, sample_list):
		#sample_list is in the format [[x11, x12, ..., x1n, y1], [x21, x22, ..., x2n, y2], ...]

		#Normalize samples
		norm_list = self.normalizer.NormalizeSampleList(sample_list)

		#Generate X and Y arrays to train
		X_train = numpy.array([[sublist[j] for j in range(len(sublist)-1)] for sublist in sample_list])
		Y_train = numpy.array([sublist[len(sublist)-1] for sublist in sample_list])

		#Train model
		with warnings.catch_warnings():
			warnings.simplefilter('ignore', ConvergenceWarning)
			self.model.fit(X_train, Y_train)

	#Use model to make prediction
	def Predict(self, parameter_list):
		#Consider parameter list not containing the answer
		X = numpy.array([self.normalizer.NormalizeSample(parameter_list)])
		answer = self.model.predict(X)[0]
		return self.normalizer.DenormalizeAtribute(answer, len(parameter_list))

	def GetMLPRegressor(self):
		#activation: ['tanh', 'relu', 'logistic', 'identity']
		#hidden_layer_sizes: [50, 100, 150, 200]
		#solver: ['lbfgs', 'sgd', 'adam']
		#alpha: [0.0001, 0.0005, 0.001, 0.005]
		#learning_rate: ['constant', 'invscaling', 'adaptative']
		act = self.param_dict['mlpar_activation']
		hl_size = self.param_dict['mlpar_hidden_layer_size']
		solv = self.param_dict['mlpar_solver']
		alp = self.param_dict['mlpar_alpha']
		lr = self.param_dict['mlpar_learning_rate']

		return MLPRegressor(max_iter=200, activation=act, hidden_layer_sizes=hl_size, solver=solv, alpha=alp, learning_rate=lr)

	def GetSVMRegressor(self):
		#C: [0.5, 1, 2, 5]
		#epsilon: [0.05, 0.1, 0.2, 0.5]
		#kernel: ['linear', 'rbf', 'sigmoid'] #'poly' and 'precomputed' don't work 
		c = self.param_dict['mlpar_C']
		e = self.param_dict['mlpar_epsilon']
		k = self.param_dict['mlpar_kernel']

		return SVR(C=c, epsilon=e, kernel=k)

	def GetKNeighborsRegressor(self):
		#n_neighbors: [1, 2, 3, 4, 5]
		#weights: ['uniform', 'distance']
		#algorithm: ['ball_tree', 'kd_tree', 'brute']
		#p: [0, 1, 2]
		n_neigh = self.param_dict['mlpar_n_neighbors']
		w = self.param_dict['mlpar_weights']
		alg = self.param_dict['mlpar_algorithm']
		p_val = self.param_dict['mlpar_p']

		return KNeighborsRegressor(n_neighbors=n_neigh, weights=w, algorithm=alg, p=p_val, n_jobs=-1)

	def GetRandomForestRegressor(self):
		#C: [1, 5, 10, 20]
		#epsilon: [0.05, 0.1, 0.2, 0.5]
		#kernel: ['linear', 'rbf', 'sigmoid'] #'poly' and 'precomputed' don't work 
		c = self.param_dict['mlpar_C']
		e = self.param_dict['mlpar_epsilon']
		k = self.param_dict['mlpar_kernel']

		return SVR(C=c, epsilon=e, kernel=k)