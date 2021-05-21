#!/usr/bin/python
# -*- coding: utf-8 -*-

from ...utils import *
from ...erb import *
from ...measurement import *

from matcher import *

#---------------------------
#Distance Grid Matcher
#Dictionary Params
	#matcher_param_distance_function: ['euclidian']
class DistanceGridMatcher(AbstractGridMatcher):

	def __init__(self, param_dict):
		AbstractGridMatcher.__init__(self, param_dict)

		if(self.param_dict['matcher_param_distance_function'] == 'euclidian'):
			self.distance_function = SquareDistance
		else:
			print 'Distance Matcher Error: unknown distance function.'
			exit()

	def Match(self, grid_list, test_sample):
		chosen_cell = grid_list[0]

		min_dist = 99999999.9
		for cell in grid_list:
			dist = self.distance_function(test_sample.rssi, cell.rssi)

			if(dist < min_dist):
				min_dist = dist
				chosen_cell = cell

		return chosen_cell