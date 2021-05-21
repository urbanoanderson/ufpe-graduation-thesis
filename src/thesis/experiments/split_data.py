#!/usr/bin/python
# -*- coding: utf-8 -*-

#Custom Classes
import sys
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *

#Utils
import random

if __name__ == "__main__":

	#Get passed parameters
	if len(sys.argv) > 2:
		TRAINING_SLICE = float(sys.argv[1])
		TEST_SLICE = float(sys.argv[2])
	else:
		TRAINING_SLICE = 0.90
		TEST_SLICE = 0.10

	#Read ERB database
	erb_list = ReadERBsFromFile('data/erbs.csv')
	
	#Read Measurement database (also calculates real pathloss)
	measurement_list = ReadMeasurementsFromFile(erb_list, 'data/samples/full.csv')

	#Shuffle data
	random.shuffle(measurement_list)

	#Partition data
	training_list = measurement_list[int(len(measurement_list) * .00) : int(len(measurement_list) * TRAINING_SLICE)]
	test_list = measurement_list[int(len(measurement_list) * TRAINING_SLICE) : int(len(measurement_list) * 1.0)]

	#Write partitions to files
	WriteMeasurementsToFile(training_list, 'data/samples/train.csv')
	WriteMeasurementsToFile(test_list, 'data/samples/test.csv')