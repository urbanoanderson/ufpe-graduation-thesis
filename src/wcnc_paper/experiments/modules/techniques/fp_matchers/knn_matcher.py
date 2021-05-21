#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy

from ...utils import *
from ...erb import *
from ...timer import *
from ...measurement import *

from matcher import *

#---------------------------
#KNN Grid Matcher
#Dictionary Params
#'matcher_param_k': int >= 1
#'matcher_param_w': int >= 0
class KNNGridMatcher(AbstractGridMatcher):

	def __init__(self, param_dict):
		AbstractGridMatcher.__init__(self, param_dict)
		self.k = self.param_dict['matcher_param_k']
		self.w = self.param_dict['matcher_param_w']

	def Match(self, grid_list, test_sample):
		#Check distance to every measurement and sort by it
		distance_function = SquareDistance
		ordered = []
		for cell in grid_list:
			dist = distance_function(cell.rssi, test_sample.rssi)
			ordered.append((dist, cell))
		ordered.sort()

		#Pick the k nearest neighbors
		neighbors = ordered[:self.k]
		numerator_lat = 0.0
		numerator_lon = 0.0
		denominator = 0.0
		for n in neighbors:
			numerator_lat += (n[1].lat * ((1.0/n[0])**self.w))
			numerator_lon += (n[1].lon * ((1.0/n[0])**self.w))
			denominator += ((1.0/n[0])**self.w)
		avg_lat = numerator_lat / denominator
		avg_lon = numerator_lon / denominator

		cell = deepcopy(neighbors[0][1])
		cell.lat = avg_lat
		cell.lon = avg_lon

		return cell