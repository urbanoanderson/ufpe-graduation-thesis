#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from ...utils import *
from ...erb import *
from ...timer import *
from ...measurement import *

#---------------------------
#Abstract Grid Trainer (Base Class)
class AbstractGridTrainer(object):

	def __init__(self, param_dict):
		self.param_dict = param_dict

	def PredictCellPathloss(self, cell, erb_list, train_list):
		raise NotImplementedError

	def TrainModel(self, erb_list, train_list):
		raise NotImplementedError

	def TrainGrid(self, grid_list, erb_list, train_list):
		#Prepare RSSI predictor model
		self.TrainModel(erb_list, train_list)

		#Use RSSI predictor model to train all grid cells
		time_count = Timer()
		time_count.Start()

		for it in range(len(grid_list)):
			grid_list[it] = self.PredictCellRSSI(grid_list[it], erb_list, train_list) 

			#Output process completeness
			percentage = (100.0*it) / float(len(grid_list))
			print "\tGrid training status: {:.2f}% ({:.2f} secs)\r".format(percentage, time_count.Elapsed()),
			if(it >= len(grid_list)-1):
				print "\tGrid training status: 100.00% ({:.2f} secs)".format(time_count.Elapsed())
			