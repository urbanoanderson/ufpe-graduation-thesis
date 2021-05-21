#!/usr/bin/python
# -*- coding: utf-8 -*-

#Custom Classes
import sys
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.normalizer import *

if __name__ == "__main__":

	#Read Samples
	erb_list = ReadERBsFromFile('data/erbs.csv')
	full_list = ReadMeasurementsFromFile(erb_list, 'data/samples/full.csv')
	
	#Create Normalizer from all the samples
	normalizer = Normalizer(full_list)
	
	#Write normalizer to file 
	normalizer.Save('data/normalizer.ini')