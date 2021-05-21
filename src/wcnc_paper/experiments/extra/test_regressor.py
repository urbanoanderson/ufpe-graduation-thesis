#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import math
import pickle

#Custom Classes
from measurement import *
from erb import *

def GetRegressorArrays(measurement_list):
	X = []
	Y = []

	for m in measurement_list:
		x_m = []
		y_m = []
		x_m.extend(m.rss)
		y_m.append(m.lat)
		y_m.append(m.lon)

		X.append(x_m)
		Y.append(y_m)

	return numpy.array(X), numpy.array(Y)

if __name__ == "__main__":

	#Read training and testing datasets from csv files
	erb_list = ReadERBsFromFile('data/erbs.csv')
	measurement_list = ReadMeasurementsFromFile(erb_list, 'data/test.csv')
	X_test, Y_test = GetRegressorArrays(measurement_list)
	
	#Load regressor
	model = pickle.load(open('data/regressor.sav', 'rb'))

	#Test against the test database
	predictions = model.predict(X_test)

	#Calculate mean distance between prediction and real values
	i = 0
	mean_dist = 0.0
	while(i < len(predictions)):
		prediction = predictions[i]
		real = Y_test[i]
		distance = DistanceInKm(prediction[0], prediction[1], real[0], real[1])
		mean_dist += distance
		i = i + 1

	mean_dist /= len(X_test)

	print(mean_dist)