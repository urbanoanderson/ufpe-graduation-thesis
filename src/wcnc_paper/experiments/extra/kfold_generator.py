#!/usr/bin/python
# -*- coding: utf-8 -*-

#Custom Classes
import sys
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.utils import *
from list_techniques import *

#Utils
import random
import datetime
import argparse

if __name__ == "__main__":

	#Get passed parameters
	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--K", type=int, help="Number K of folds", default=10)
	parser.add_argument("-r", "--GridResolution", type=int, help="Resolution used for the grid", default=50)
	parser.add_argument("-g", "--GenerateFolds", type=bool, help="If the script should generate new folds", default=False)
	args = parser.parse_args()

	K = args.K
	GRID_POINTS_FILE = "data/grid_points/squaremap_{}m.json".format(args.GridResolution)

	#Opens log file
	verbose = True
	log = True
	log_file = None
	if(log):
		d = datetime.datetime.now()
		log_file = open("log/datetime{}{}{}{}{}_kfold{}_res{}.log".format(d.year, str(d.month).zfill(2), str(d.day).zfill(2), str(d.hour).zfill(2), str(d.minute).zfill(2), K, args.GridResolution), "w")

	#Read ERB database
	erb_list = ReadERBsFromFile('data/erbs.csv')

	#Generate K Folds
	if(args.GenerateFolds):
		#Read All Measurement database
		full_list = ReadMeasurementsFromFile(erb_list, 'data/samples/full.csv')

		#Shuffle data
		random.shuffle(full_list)

		#Partition data in K folds
		folds = SplitKfold(full_list, K)
		
		#Write all folds to files for saving experiment parameters
		for i in range(len(folds)):
			WriteMeasurementsToFile(folds[i], "data/samples/kfolds/fold_{}.csv".format(i))
	else:
		folds = []
		for i in range(K):
			fold = ReadMeasurementsFromFile(erb_list, "data/samples/kfolds/fold_{}.csv".format(i))
			folds.append(fold)

	#Execute Kfold experiment
	for i in range(0, K):

		PrintAndLog("\n>>>KFOLD ITERATION: {}\n".format(i), log_file, verbose)

		#Initialize train and test lists for iteration
		train_list = []
		test_list = []
		for j in range(len(folds)):
			if i != j:
				train_list.extend(folds[j])
			else:
				test_list.extend(folds[j])

		#Get technique list used
		technique_list = GetTechniques(erb_list, GRID_POINTS_FILE)

		#Train and Test techniques
		for tech in technique_list:

			PrintAndLog("\tTECHNIQUE NAME: {}".format(tech.name), log_file, verbose)

			#Train technique
			tech.param_dict['grid_filename'] = tech.param_dict['tech_folder'] + "kfold_it{}_res{}_".format(i, args.GridResolution) + tech.param_dict['tech_name'] + ".csv" 
			tech.Train(train_list)
			tech.Save()

			#Test technique
			#results are in the format: [mean_error, rms_error, deviation, variance]
			results = tech.TestList(test_list)

			#Print technique results
			PrintAndLog("\tERROR RESULTS IN KM(μ, rms, σ, v): [{:.3f}, {:.3f}, {:.3f}, {:.3f}]".format(results[0], results[1], results[2], results[3]), log_file, verbose)

	#Close log file after experiment
	if log_file != None and (not log_file.closed):
		log_file.close()