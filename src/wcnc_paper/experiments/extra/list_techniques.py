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
	param_k = [3]#[1,2,3,4,5]
	param_w = [1]#[0,1,2,3]

	for k in param_k:
		for w in param_w:
			if(not (k == 1 and w > 0)):
				technique = FingerprintingTechnique(erb_list)
				technique.SetName("Fingerprinting KNN (K={}, W={})".format(k, w))
				param_dict = {}
				param_dict['tech_name'] = "knn-k{}-w{}".format(k,w)
				param_dict['grid_points_filename'] = grid_points_file
				param_dict['grid_filename'] = "data/technique_data/fp_knn/grid_k{}-w{}.csv".format(k, w)
				param_dict['grid_trainer'] = 'knn'
				param_dict['param_k'] = k
				param_dict['param_w'] = w

				param_dict['grid_matcher'] = 'distance'
				param_dict['matcher_param_distance_function'] = 'euclidian'

				technique.SetParams(param_dict)
				technique_list.append(technique)

	#Return all the techniques
	return technique_list