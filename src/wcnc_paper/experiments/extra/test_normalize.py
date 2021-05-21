#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import sys
import numpy
import warnings
from sklearn import preprocessing
from sklearn.exceptions import ConvergenceWarning
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *

#/////////////////////////////////////////////
class Normalizer(object):

	def __init__(self, sample_list):
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
		for i in range(len(sample.rssi)):
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

#/////////////////////////////////////////////

if __name__ == "__main__":

	#mat = [
	#[8.0,3.0,5.0,9.0],
	#[7.0,6.0,2.0,1.0],
	#[9.0,8.0,6.0,2.0],
	#[5.0,6.0,4.0,7.0],
	#]

	#a = numpy.array(mat)
	#print a
	#scaler = preprocessing.MinMaxScaler().fit(a)
	#b = scaler.transform(a)
	#print b
	#c = numpy.array([[10.0, 5.0, 3.0, 0.0]])
	#print scaler.transform(c)
	#exit()

	#scaler = preprocessing.MinMaxScaler().fit(mat)
	#s = [5,3,4,8]
	#s = scaler.transform(s)
	#print s
	#s = scaler.inverse_transform(s)
	#print s
	#s.reshape(1, -1)
	#print s

	#exit()

	#////////////////////////////////

	#Read ERB database
	erb_list = ReadERBsFromFile('data/erbs.csv')
	
	#Read Measurement database (also calculates real pathloss)
	full_list = ReadMeasurementsFromFile(erb_list, 'data/samples/full.csv')
	train_list = ReadMeasurementsFromFile(erb_list, 'data/samples/train.csv')
	test_list = ReadMeasurementsFromFile(erb_list, 'data/samples/test.csv')

	#Initialize normalizer
	#scaler = GetScaler(full_list) 
	normalizer = Normalizer(full_list)

	#---------------------------------------------------------------------
	#TRAIN MODEL FOR EACH ERB
	#---------------------------------------------------------------------
	
	models = []
	for i in range(len(erb_list)):
			
			#Initialize Model
			model = SVR(C=1, epsilon=0.1, kernel='poly')
			#model = MLPRegressor(max_iter=200, solver='adam', alpha=0.0001, 
			#	activation='relu',
			#	hidden_layer_sizes=200,
			#	learning_rate='constant'
			#)

			#Create sample_list is in the format [[x11, x12, ..., x1n, y1], [x21, x22, ..., x2n, y2], ...]
			sample_list = []
			for m in train_list:
				m = normalizer.NormalizeSample(m)
				parameter_list = [m.lat, m.lon, m.rssi[i]]
				sample_list.append(parameter_list)

			#Generate X and Y arrays to train
			X_train = numpy.array([[sublist[j] for j in range(len(sublist)-1)] for sublist in sample_list])
			Y_train = numpy.array([sublist[len(sublist)-1] for sublist in sample_list])

			#Train model
			with warnings.catch_warnings():
				warnings.simplefilter('ignore', ConvergenceWarning)
				warnings.simplefilter('ignore', DeprecationWarning)
				model.fit(X_train, Y_train)

			#Stores the ERB model
			models.append(model)

	#---------------------------------------------------------------------
	#TEST MODEL FOR SAMPLES
	#---------------------------------------------------------------------

	cell = test_list[0]

	print "------------------------"
	print "Original Sample: {}".format(cell)
	print "------------------------"

	cell = normalizer.NormalizeSample(test_list[0])
	atributes = [cell.lat, cell.lon]
	X = numpy.array(atributes)

	print "------------------------"
	print "Normalized Sample: {}".format(cell)
	print "------------------------"

	for i in range(len(erb_list)):
		with warnings.catch_warnings():
			warnings.simplefilter('ignore', DeprecationWarning)
			cell.rssi[i] = models[i].predict(X)[0]

	print "------------------------"
	print "Output Normalized Sample: {}".format(cell)
	print "------------------------"
	print "Output Denormalized Sample: {}".format(normalizer.DenormalizeSample(cell))
	print "------------------------"