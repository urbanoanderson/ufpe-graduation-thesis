#!/usr/bin/python
# -*- coding: utf-8 -*-

from ...utils import *
from ...erb import *
from ...timer import *
from ...measurement import *

#---------------------------
#Abstract Grid Matcher (Base Class)
class AbstractGridMatcher(object):

	def __init__(self, param_dict):
		self.param_dict = param_dict

	def Match(self, grid_list, test_sample):
		raise NotImplementedError
			