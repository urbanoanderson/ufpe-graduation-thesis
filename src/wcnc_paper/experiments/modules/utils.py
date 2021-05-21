#!/usr/bin/python
# -*- coding: utf-8 -*-

#Standart libs
import re
import math
import numpy
import random

#Print to screen and write to file
def PrintAndLog(str_message, f_log, verbose=True):
	if verbose:
		print str_message
	if(f_log != None):
		f_log.write(str_message + '\n')

#Split a list of samples in K folds
def SplitKfold(samples, K):
	avg = len(samples) / float(K)
	out = []
	last = 0.0
	while last < len(samples):
		out.append(samples[int(last):int(last + avg)])
		last += avg
	return out

#Distance in km between two geografic coordenates
def DistanceInKm(latA, lonA, latB, lonB):
	lat1 = latA
	lon2 = lonA
	lat2 = latB
	lon1 = lonB
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2]) 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a)) 
	km = 6367 * c
	return km

def DistanceLat(latA, lonA, latB, lonB):
	return DistanceInKm(latA, lonA, latB, lonA)

def DistanceLon(latA, lonA, latB, lonB):
	return DistanceInKm(latA, lonA, latA, lonB)

#Distance metrics
def SquareDistance(valuesA, valuesB):
	dist = 0
	for i in range(len(valuesA)):
		dist += (valuesA[i]-valuesB[i])*(valuesA[i]-valuesB[i])
	return dist

def ManhattanDistance(valuesA, valuesB):
	dist = 0
	for i in range(len(valuesA)):
		dist += math.fabs(valuesA[i]-valuesB[i])
	return dist

#Alphanumeric String Sorting
def atoi(text):
	return int(text) if text.isdigit() else text 

def natural_keys(text):
	return [ atoi(c) for c in re.split('(\d+)', text) ]