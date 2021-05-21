#!/usr/bin/python
# -*- coding: utf-8 -*-

#Custom Classes
from modules.techniques.technique import *
from modules.techniques.fp_technique import *

def GetTechniques(erb_list, grid_points_file):

	#Put all techniques in a list
	technique_list = []

	#---------------------------------------------------------------------
	#FINGERPRINTING TECHNIQUES
	#---------------------------------------------------------------------

	#Fingerprinting KNN
	param_k = [1,2,3,4,5]
	param_w = [0,1,2,3]

	for k in param_k:
		for w in param_w:
			if(not (k == 1 and w > 0)):
				technique = FingerprintingTechnique(erb_list)
				technique.SetName("Fingerprinting KNN (K={}, W={})".format(k, w))
				param_dict = {}
				param_dict['tech_name'] = "knn-k{}-w{}".format(k,w)
				param_dict['tech_folder'] = "data/technique_data/fp_knn/"
				param_dict['grid_points_filename'] = grid_points_file
				param_dict['grid_filename'] = param_dict['tech_folder'] + "grid_k{}-w{}.csv".format(k, w)
				param_dict['grid_trainer'] = 'knn'
				param_dict['param_k'] = k
				param_dict['param_w'] = w
				technique.SetParams(param_dict)
				technique_list.append(technique)

	#MLP
	param_activation_function = ['identity', 'logistic', 'tanh', 'relu']
	param_learning_rate = ['constant', 'invscaling', 'adaptive']
	param_hidden_layer_size = [50, 100, 200, 500]

	for act in param_activation_function:
		for lr in param_learning_rate:
			for hls in param_hidden_layer_size:
				technique = FingerprintingTechnique(erb_list)
				technique.SetName("Fingerprinting MLP (Act={}, LR={}, HLS={})".format(act, lr, hls))
				param_dict = {}
				param_dict['tech_name'] = "mlp-act{}-lr{}-hls{}".format(act, lr, hls)
				param_dict['tech_folder'] = "data/technique_data/fp_mlp/"
				param_dict['normalizer_file'] = "data/normalizer.ini"
				param_dict['grid_points_filename'] = grid_points_file
				param_dict['grid_filename'] = param_dict['tech_folder'] + "grid_act{}-lr{}-hls{}.csv".format(act, lr, hls)
				param_dict['grid_trainer'] = 'mlp'
				param_dict['param_activation_function'] = act
				param_dict['param_learning_rate'] = lr
				param_dict['param_hidden_layer_size'] = hls
				technique.SetParams(param_dict)
				technique_list.append(technique)

	#SVM
	param_kernel = ['poly', 'rbf', 'linear', 'sigmoid']
	param_c = [0.5, 1, 2, 5]
	param_e = [0.05, 0.1, 0.2, 0.5]

	for kernel in param_kernel:
		for C in param_c:
			for e in param_e:
				technique = FingerprintingTechnique(erb_list)
				technique.SetName("Fingerprinting SVM (Kernel={}, C={}, e={})".format(kernel, C, e))
				param_dict = {}
				param_dict['tech_name'] = "svm-kernel{}-C{}-e{}".format(kernel, C, e)
				param_dict['tech_folder'] = "data/technique_data/fp_svm/"
				param_dict['normalizer_file'] = "data/normalizer.ini"
				param_dict['grid_points_filename'] = grid_points_file
				param_dict['grid_filename'] = param_dict['tech_folder'] + "grid_kernel{}-C{}-e{}.csv".format(kernel, C, e)
				param_dict['grid_trainer'] = 'svm'
				param_dict['param_kernel'] = kernel
				param_dict['param_c'] = C
				param_dict['param_e'] = e
				technique.SetParams(param_dict)
				technique_list.append(technique)

	#Random Forest
	param_n_estimators = [10, 20, 50, 75, 100]

	for n_estimators in param_n_estimators:
		technique = FingerprintingTechnique(erb_list)
		technique.SetName("Fingerprinting Random Forest (n_estimators={})".format(n_estimators))
		param_dict = {}
		param_dict['tech_name'] = "rf-n_estimators{}".format(n_estimators)
		param_dict['tech_folder'] = "data/technique_data/fp_rf/"
		param_dict['grid_points_filename'] = grid_points_file
		param_dict['grid_filename'] = param_dict['tech_folder'] + "grid_n_estimators{}.csv".format(n_estimators)
		param_dict['grid_trainer'] = 'rf'
		param_dict['param_n_estimators'] = n_estimators
		technique.SetParams(param_dict)
		technique_list.append(technique)

	#----------------------------------------------------
	#Mockup Techniques for tests
	#----------------------------------------------------

	#Random Forest
	# param_n_estimators = [75]

	# for n_estimators in param_n_estimators:
	# 	technique = FingerprintingTechnique(erb_list)
	# 	technique.SetName("Fingerprinting Random Forest (n_estimators={})".format(n_estimators))
	# 	param_dict = {}
	# 	param_dict['tech_name'] = "rf-n_estimators{}".format(n_estimators)
	# 	param_dict['tech_folder'] = "data/technique_data/fp_rf/"
	# 	param_dict['grid_points_filename'] = grid_points_file
	# 	param_dict['grid_filename'] = param_dict['tech_folder'] + "grid_n_estimators{}.csv".format(n_estimators)
	# 	param_dict['grid_trainer'] = 'rf'
	# 	param_dict['param_n_estimators'] = n_estimators
	# 	technique.SetParams(param_dict)
	# 	technique_list.append(technique)

	# #Fingerprinting KNN
	# param_k = [3,5]
	# param_w = [0]

	# for k in param_k:
	# 	for w in param_w:
	# 		if(not (k == 1 and w > 0)):
	# 			technique = FingerprintingTechnique(erb_list)
	# 			technique.SetName("Fingerprinting KNN (K={}, W={})".format(k, w))
	# 			param_dict = {}
	# 			param_dict['tech_name'] = "knn-k{}-w{}".format(k,w)
	# 			param_dict['tech_folder'] = "data/technique_data/fp_knn/"
	# 			param_dict['grid_points_filename'] = grid_points_file
	# 			param_dict['grid_filename'] = param_dict['tech_folder'] + "grid_{}.csv".format(param_dict['tech_name'])
	# 			param_dict['grid_trainer'] = 'knn'
	# 			param_dict['param_k'] = k
	# 			param_dict['param_w'] = w
	# 			technique.SetParams(param_dict)
	# 			technique_list.append(technique)

	# #K Neighbors
	# for n_neigh in [1, 2, 3, 4, 5]:
	# 	for w in ['uniform', 'distance']:
	# 		for alg in ['ball_tree', 'kd_tree', 'brute']:
	# 			for p in [1, 2]:
	# 				technique = FingerprintingTechnique(erb_list)
	# 				technique.SetName("K neighbors [{} {} {} {}]".format(n_neigh, w, alg, p))
	# 				param_dict = {}
	# 				param_dict['tech_folder'] = "data/technique_data/fp_ml/"
	# 				param_dict['grid_points_filename'] = grid_points_file
	# 				param_dict['grid_filename'] = param_dict['tech_folder'] + "grid_{}_{}_{}_{}.csv".format(n_neigh, w, alg, p)
	# 				param_dict['norm_file'] = 'none'
	# 				param_dict['grid_trainer'] = 'ml'
	# 				param_dict['ml_algorithm'] = 'k_neighbors'
	# 				param_dict['mlpar_n_neighbors'] = n_neigh
	# 				param_dict['mlpar_weights'] = w
	# 				param_dict['mlpar_algorithm'] = alg
	# 				param_dict['mlpar_p'] = p
	# 				technique.SetParams(param_dict)
	# 				technique_list.append(technique)

	#---------------------------------------------------------------------

	#Return all the techniques
	return technique_list