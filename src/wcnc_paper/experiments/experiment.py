#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import sys
import datetime
import copy

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.timer import *
from modules.utils import *
from modules.techniques.technique import *
from modules.techniques.fp_technique import *


def GetTechnique(param_k=3, param_w=1):
	technique = FingerprintingTechnique(erb_list)	
	param_dict = {}
	param_dict['grid_matcher'] = 'distance'
	param_dict['matcher_param_distance_function'] = 'euclidian'

	#SVM TRAINER
	# param_dict['grid_trainer'] = 'svm'
	# param_dict['trainer_param_kernel'] = 'rbf' #['rbf', 'linear', 'sigmoid', 'poly']
	# param_dict['trainer_param_c'] = [16, 16, 16, 16, 32, 16]
	# param_dict['trainer_param_e'] = 0.1

	#RANDOM FOREST TRAINER
	#param_dict['grid_trainer'] = 'rf'
	#param_dict['trainer_param_n_estimators'] = 30

	#KNN TRAINER
	param_dict['grid_trainer'] = 'knn'
	param_dict['trainer_param_k'] = param_k
	param_dict['trainer_param_w'] = param_w
	
	technique.SetTrainerParams(param_dict)
	technique.SetMatcherParams(param_dict)

	return technique


if __name__ == "__main__":

	#Experiment Parameters
	generate_folds = False
	save_trained_grids = False
	verbose = True
	log_output = True
	num_k_folds = 10
	erb_file = 'data/erbs/erbs_big.csv'
	full_measurements_file = 'data/samples/full_big.csv'
	grid_points_files = [
							#['data/grid_points/roadmap_small_20m.json', 'roadSmall20m'],
							#['data/grid_points/squaremap_small_20m.json', 'squareSmall20m']

							# ['data/grid_points/roadmap_big_1m.json', 'roadBig1m'],
							# ['data/grid_points/roadmap_big_2m.json', 'roadBig2m'],
							# ['data/grid_points/roadmap_big_3m.json', 'roadBig3m'],
							# ['data/grid_points/roadmap_big_4m.json', 'roadBig4m'],
							# ['data/grid_points/roadmap_big_5m.json', 'roadBig5m'],
							# ['data/grid_points/roadmap_big_6m.json', 'roadBig6m'],
							# ['data/grid_points/roadmap_big_7m.json', 'roadBig7m'],
							# ['data/grid_points/roadmap_big_8m.json', 'roadBig8m'],
							# ['data/grid_points/roadmap_big_9m.json', 'roadBig9m'],
							# ['data/grid_points/roadmap_big_10m.json', 'roadBig10m'],
							# ['data/grid_points/roadmap_big_11m.json', 'roadBig11m'],
							# ['data/grid_points/roadmap_big_12m.json', 'roadBig12m'],
							# ['data/grid_points/roadmap_big_13m.json', 'roadBig13m'],
							# ['data/grid_points/roadmap_big_14m.json', 'roadBig14m'],
							# ['data/grid_points/roadmap_big_15m.json', 'roadBig15m'],
							# ['data/grid_points/roadmap_big_16m.json', 'roadBig16m'],
							# ['data/grid_points/roadmap_big_17m.json', 'roadBig17m'],
							# ['data/grid_points/roadmap_big_18m.json', 'roadBig18m'],
							# ['data/grid_points/roadmap_big_19m.json', 'roadBig19m'],
							#['data/grid_points/roadmap_big_20m.json', 'roadBig20m'],

							['data/grid_points/new_roadmap_big_10m.json', 'newRoadBig10m'],
							['data/grid_points/new_roadmap_big_20m.json', 'newRoadBig20m'],

							#['data/grid_points/squaremap_big_1m.json', 'squareBig1m'],
							#['data/grid_points/squaremap_big_2m.json', 'squareBig2m'],
							#['data/grid_points/squaremap_big_3m.json', 'squareBig3m'],
							#['data/grid_points/squaremap_big_4m.json', 'squareBig4m'],
							#['data/grid_points/squaremap_big_5m.json', 'squareBig5m'],
							#['data/grid_points/squaremap_big_6m.json', 'squareBig6m'],
							#['data/grid_points/squaremap_big_7m.json', 'squareBig7m'],
							#['data/grid_points/squaremap_big_8m.json', 'squareBig8m'],
							#['data/grid_points/squaremap_big_9m.json', 'squareBig9m']
							['data/grid_points/squaremap_big_10m.json', 'squareBig10m'],
							#['data/grid_points/squaremap_big_11m.json', 'squareBig11m'],
							#['data/grid_points/squaremap_big_12m.json', 'squareBig12m'],
							#['data/grid_points/squaremap_big_13m.json', 'squareBig13m'],
							#['data/grid_points/squaremap_big_14m.json', 'squareBig14m'],
							#['data/grid_points/squaremap_big_15m.json', 'squareBig15m'],
							#['data/grid_points/squaremap_big_16m.json', 'squareBig16m'],
							#['data/grid_points/squaremap_big_17m.json', 'squareBig17m'],
							#['data/grid_points/squaremap_big_18m.json', 'squareBig18m'],
							#['data/grid_points/squaremap_big_19m.json', 'squareBig19m'],
							['data/grid_points/squaremap_big_20m.json', 'squareBig20m']
						]

	#Read erb file
	erb_list = ReadERBsFromFile(erb_file)

	#Generate K Folds
	if(generate_folds):
		
		#Read All Measurement database
		full_list = ReadMeasurementsFromFile(erb_list, full_measurements_file)

		#Shuffle data
		random.shuffle(full_list)

		#Partition data in K folds
		folds = SplitKfold(full_list, num_k_folds)
		
		#Write all folds to files for saving experiment parameters
		for i in range(len(folds)):
			WriteMeasurementsToFile(folds[i], "data/samples/kfolds/fold_{}.csv".format(i))

	#Don't generate new folds (use old folds)		
	else:
		folds = []
		for i in range(num_k_folds):
			fold = ReadMeasurementsFromFile(erb_list, "data/samples/kfolds/fold_{}.csv".format(i))
			folds.append(fold)

	#Opens log file
	log_file = None
	if(log_output):
		d = datetime.datetime.now()
		log_file = open("log/experiment_%s-%s-%s__%s-%s.log" % (d.day, d.month, d.year, d.hour, d.minute), "w")

	#-------------------------------------------------------------------------
	#Check Pathloss Error
	
	# print("WKNN AVERAGE RSSI ERROR FOR EACH ERB")
	# for param_k in range(1,6):
	# 	for param_w in range(0,4):
	# 		kfold_average_error = [0.0 for x in range(len(erb_list))]
	# 		for kfold_it in range(0, num_k_folds):

	# 			#Select folds used for training and testing
	# 			train_list = []
	# 			test_list = []
	# 			for j in range(len(folds)):
	# 				if kfold_it != j:
	# 					train_list.extend(folds[j])
	# 				else:
	# 					test_list.extend(folds[j])

	# 			technique = GetTechnique(param_k, param_w)

	# 			technique.grid_trainer.TrainModel(erb_list, train_list)

	# 			sample_errors = []
	# 			avg_sample_error = [0.0 for x in range(len(erb_list))]
	# 			for m in test_list:
	# 				res = technique.grid_trainer.PredictCellRSSI(copy.deepcopy(m), erb_list, train_list)

	# 				sample_error = []
	# 				for i in range(len(erb_list)):
	# 					error = abs(m.rssi[i]-res.rssi[i])
	# 					sample_error.append(error)
	# 					avg_sample_error[i] += error

	# 				sample_errors.append(sample_error)

	# 			for i in range(len(erb_list)):
	# 				avg_sample_error[i] /= len(test_list)
	# 				kfold_average_error[i] += avg_sample_error[i]

	# 		for i in range(len(erb_list)):
	# 			kfold_average_error[i] /= num_k_folds

	# 		print("K={},W={}: {}\n".format(param_k, param_w, kfold_average_error))
			
	# exit()

	#-------------------------------------------------------------------------

	kfold_avg_results = [[0.0,0.0,0.0,0.0] for x in range(len(grid_points_files))] #[[0.0, 0.0, 0.0, 0.0]]*len(grid_points_files)

	#Execute Kfold experiment
	for kfold_it in range(0, num_k_folds):

		PrintAndLog("\nKFOLD ITERATION: {}\n".format(kfold_it), log_file, verbose)

		#Select folds used for training and testing
		train_list = []
		test_list = []
		for j in range(len(folds)):
			if kfold_it != j:
				train_list.extend(folds[j])
			else:
				test_list.extend(folds[j])

		#Do experiment for each grid file
		for idx_file, grid_points_file in enumerate(grid_points_files):

			PrintAndLog("\tGRID FILE: {}".format(grid_points_file[0]), log_file, verbose)

			technique = GetTechnique()

			#Train grid with technique
			technique.Train(train_list, grid_points_file[0])
			if(save_trained_grids == True):
				technique.Save("data/technique_data/fp/trained_grid_kfold{}_{}.csv".format(kfold_it, grid_points_file[1]))

			#Test trained grid and collect results
			results = technique.TestListFilter(test_list) #format: [mean_error, rms_error, deviation, variance]

			#Print results for this grid file
			PrintAndLog("\tERROR RESULTS IN KM(μ, rms, σ, v): [{}, {}, {}, {}]\n".format(results[0]*1000, results[1]*1000, results[2]*1000, results[3]*1000), log_file, verbose)

			for x in range(4):
				kfold_avg_results[idx_file][x] += results[x]

	
	for x in range(len(grid_points_files)):
		for y in range(4):
			kfold_avg_results[x][y] /= num_k_folds
		PrintAndLog("\n>>KFOLD RESULTS IN KM(file, μ, rms, σ, v): [{}, {}, {}, {}, {}]\n".format(grid_points_files[x][1], kfold_avg_results[x][0]*1000, kfold_avg_results[x][1]*1000, kfold_avg_results[x][2]*1000, kfold_avg_results[x][3]*1000), log_file, verbose)

	#-------------------------------------------------------------------------

	#Close log file after experiment
	if log_file != None and (not log_file.closed):
		log_file.close()