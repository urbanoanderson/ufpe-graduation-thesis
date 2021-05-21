#!/usr/bin/python
# -*- coding: utf-8 -*-

#Utils
import sys
import ast
from pprint import pprint
sys.dont_write_bytecode = True

def mean(a):
    return sum(a) / len(a)

if __name__ == "__main__":

	#-----------------------------------------------
	#PARAMETERS
	#-----------------------------------------------
	K = 10
	NUM_TECHNIQUES = 134
	#LOG_FILE = "log/teste.log"
	LOG_FILE = "log/30m.log"

	#-----------------------------------------------
	#READ ITERATION RESULTS FROM FILE
	#-----------------------------------------------
	results = []
	f = open(LOG_FILE, "r")
	if(not f.closed):
		for k in range(K):
			f.readline()	#ignore first blank line
			f.readline()	#ignore iteration line
			f.readline()	#ignore second blank line
			it_results = []
			for i in range(NUM_TECHNIQUES):
				nameline = f.readline()
				tech_name = nameline.split("TECHNIQUE NAME: ")[1]
				resultline = f.readline()
				resultstr = resultline.split("ERROR RESULTS IN KM(μ, rms, σ, v): ")[1]
				resultlist = ast.literal_eval(resultstr)
				it_results.append( [tech_name, resultlist] )
			results.append(it_results)
		f.close()
	else:
		print ("Error. File " + LOG_FILE + " could not be opened.");
		exit()

	#-----------------------------------------------
	#PROCESS RESULTS
	#-----------------------------------------------

	avg_results = []
	for t in range(NUM_TECHNIQUES):
		t_results = [r[t][1] for r in results]
		t_avg = map(mean, zip(*t_results))
		avg_results.append(t_avg)

	tech_names = [r[0].strip() for r in results[0]]

	ordered_results = []
	for i in range(len(avg_results)):
		ordered_results.append([tech_names[i], avg_results[i]])
	ordered_results.sort(key=lambda x: x[1][0])

	#-----------------------------------------------
	#PRINT AVERAGE RESULTS
	#-----------------------------------------------
	# print("AVERAGE RESULTS:\n")

	# for i in range(len(avg_results)):
	# 	print("{} & {} & {} & {} & {} \\\\".format(tech_names[i], 
	# 		int(avg_results[i][0]*1000),
	# 		int(avg_results[i][1]*1000),
	# 		int(avg_results[i][2]*1000),
	# 		int(avg_results[i][3]*1000)))

	print("ORDERED:\n")
	#pprint(ordered_results)

	for i in range(len(avg_results)):
		print("{} & {} & {} & {} & {} \\\\".format(ordered_results[i][0], 
			int(ordered_results[i][1][0]*1000),
			int(ordered_results[i][1][1]*1000),
			int(ordered_results[i][1][2]*1000),
			int(ordered_results[i][1][3]*1000)))