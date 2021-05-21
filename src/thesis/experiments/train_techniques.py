#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import sys

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.techniques.technique import *


if __name__ == "__main__":

	#Get passed parameters
	if len(sys.argv) > 1:
		GRID_POINTS_FILE = sys.argv[1]
	else:
		GRID_POINTS_FILE = 'data/grid_points/squaremap_50m.json'

	#Set script arguments
	train_sample_folder = 'data/samples/'
	train_file = 'train.csv'

	#Print file used
	print("TRAIN FILE:")
	print("\t`{}`\n".format(train_file))

	#Read training dataset from csv file
	erb_list = ReadERBsFromFile('data/erbs.csv')
	train_list = ReadMeasurementsFromFile(erb_list, train_sample_folder + train_file)

	#Put all techniques in a list
	from list_techniques import *
	technique_list = GetTechniques(erb_list, GRID_POINTS_FILE)

	#Train and Save all techniques
	for tech in technique_list:
		print("TRAINING TECHNIQUE: {}".format(tech.name))
		tech.Train(train_list)
		tech.Save()

	#Close log file after experiment
	if log_file != None and (not log_file.closed):
		log_file.close()