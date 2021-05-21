#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from ...utils import *
from ...erb import *
from ...timer import *
from ...measurement import *

from trainer import *

#---------------------------
#KNN Grid Trainer
#Dictionary Params
#'param_k': int >= 1
#'param_w': int >= 0
class KNNGridTrainer(AbstractGridTrainer):

	def __init__(self, param_dict):
		AbstractGridTrainer.__init__(self, param_dict)
		self.k = self.param_dict['param_k']
		self.w = self.param_dict['param_w']

	def TrainModel(self, erb_list, train_list):
		"\tInitializing KNN model..."

	def PredictCellRSSI(self, cell, erb_list, train_list):
		#Check distance to every measurement and sort by it
		ordered = []
		for m in train_list:
			dist = DistanceInKm(m.lat, m.lon, cell.lat, cell.lon)
			ordered.append((dist, m))
		ordered.sort()

		#Pick the k nearest neighbors and average their rssi
		neighbors = ordered[:self.k]
		for i in range(len(erb_list)):
			numerator = 0.0
			denominator = 0.0
			for n in neighbors:
				numerator += (n[1].rssi[i] * ((1.0/n[0])**self.w))
				denominator += ((1.0/n[0])**self.w)
			avg_rssi = numerator / denominator

			cell.rssi[i] = avg_rssi

		return cell