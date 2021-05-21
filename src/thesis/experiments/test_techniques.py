#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import sys
import datetime

#Custom Classes
sys.dont_write_bytecode = True
from modules.erb import *
from modules.measurement import *
from modules.timer import *
from modules.utils import *
from modules.techniques.technique import *


if __name__ == "__main__":

	#Get passed parameters
	if len(sys.argv) > 1:
		GRID_POINTS_FILE = sys.argv[1]
	else:
		GRID_POINTS_FILE = 'data/grid_points/squaremap_50m.json'

	#Set script arguments
	test_sample_folder = 'data/samples/'
	test_file = 'test.csv'
	verbose = True
	log = True
	
	#Read training dataset from csv file
	erb_list = ReadERBsFromFile('data/erbs.csv')
	test_list = ReadMeasurementsFromFile(erb_list, test_sample_folder + test_file)

	#Opens log file
	log_file = None
	if(log):
		d = datetime.datetime.now()
		log_file = open("log/test_%s-%s-%s__%s:%s.log" % (d.day, d.month, d.year, d.hour, d.minute), "w")

	#Put all techniques in a list
	from list_techniques import *
	technique_list = GetTechniques(erb_list, GRID_POINTS_FILE)

	#Test a measure set with every technique
	PrintAndLog("TEST FILE:", log_file, verbose)
	PrintAndLog("\t`{}`\n".format(test_file), log_file, verbose)
	PrintAndLog("NUMBER OF TECHNIQUES:", log_file, verbose)
	PrintAndLog("\t{}\n".format(len(technique_list)), log_file, verbose)
	PrintAndLog("INDIVIDUAL RESULTS:", log_file, verbose)
	time_count = Timer()
	time_count.Start()
	ordered = []
	for tech in technique_list:
		tech.Load()
		results = tech.TestList(test_list)
		ordered.append( (tech.name, results ) )

		#Print technique results
		PrintAndLog("\tTECHNIQUE NAME: {}".format(tech.name), log_file, verbose)
		PrintAndLog("\t[MIN ERROR: {:.3f} km, MAX ERROR: {:.3f} km, AVG ERROR: {:.3f} km, RMS ERROR: {:.3f} km]".format(results[0], results[1], results[2], results[3]), log_file, verbose)

	#Print time spent testing all algorithms
	elapsed_time = int(time_count.Elapsed())
	minutes = elapsed_time / 60
	seconds = elapsed_time - minutes*60
	PrintAndLog("\nELAPSED TIME:", log_file, verbose)
	PrintAndLog("\t{}m {}s\n".format(minutes, seconds), log_file, verbose)

	#Print best algorithm for each metric
	PrintAndLog("BEST RESULTS:", log_file, verbose)

	ordered.sort(key=lambda x: x[1][0])
	PrintAndLog("\tBEST BY MIN ERROR: {}".format(ordered[0][0]), log_file, verbose)
	PrintAndLog("\t[MIN ERROR: {:.3f} km, MAX ERROR: {:.3f} km, AVG ERROR: {:.3f} km, RMS ERROR: {:.3f} km]".format(ordered[0][1][0], ordered[0][1][1], ordered[0][1][2], ordered[0][1][3]), log_file, verbose)

	ordered.sort(key=lambda x: x[1][1])
	PrintAndLog("\tBEST BY MAX ERROR: {}".format(ordered[0][0]), log_file, verbose)
	PrintAndLog("\t[MIN ERROR: {:.3f} km, MAX ERROR: {:.3f} km, AVG ERROR: {:.3f} km, RMS ERROR: {:.3f} km]".format(ordered[0][1][0], ordered[0][1][1], ordered[0][1][2], ordered[0][1][3]), log_file, verbose)

	ordered.sort(key=lambda x: x[1][2])
	PrintAndLog("\tBEST BY AVG ERROR: {}".format(ordered[0][0]), log_file, verbose)
	PrintAndLog("\t[MIN ERROR: {:.3f} km, MAX ERROR: {:.3f} km, AVG ERROR: {:.3f} km, RMS ERROR: {:.3f} km]".format(ordered[0][1][0], ordered[0][1][1], ordered[0][1][2], ordered[0][1][3]), log_file, verbose)

	ordered.sort(key=lambda x: x[1][3])
	PrintAndLog("\tBEST BY RMS ERROR: {}".format(ordered[0][0]), log_file, verbose)
	PrintAndLog("\t[MIN ERROR: {:.3f} km, MAX ERROR: {:.3f} km, AVG ERROR: {:.3f} km, RMS ERROR: {:.3f} km]".format(ordered[0][1][0], ordered[0][1][1], ordered[0][1][2], ordered[0][1][3]), log_file, verbose)

	#Close log file after experiment
	if log_file != None and (not log_file.closed):
		log_file.close()