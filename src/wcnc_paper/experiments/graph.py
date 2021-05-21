#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#Custom Classes
sys.dont_write_bytecode = True

if __name__ == "__main__":

	#-----------------------------------------------------
	#INPUT ARRAYS
	#-----------------------------------------------------
	resolution = [1, 2, 3, 4, 5]
	precision_road = [40, 42, 43, 45, 48]
	precision_square = [50, 49, 52, 55, 56]

	#-----------------------------------------------------
	#PLOT DATA
	#-----------------------------------------------------
	title = ""
	x_title = "Resolution"
	y_title = "Precision"
	x_axis = resolution
	y_axis = precision_road
	filename = "doc/visualization/graph.png"

	fig = plt.figure(1, figsize = (16,9))
	ax = fig.add_subplot(111);
	padding_x = 0
	padding_y = 1
	ax.set_xlim([min(x_axis)-padding_x, max(x_axis)+padding_x])
	ax.set_ylim([min(precision_road+precision_square)-padding_y, max(precision_road+precision_square)+padding_y])
	ax.set_xlabel(x_title);
	ax.set_ylabel(y_title);
	ax.grid(False);
	plt.suptitle(title)
	plt.plot(x_axis, precision_road, color='red', linestyle='--', marker='o')
	plt.plot(x_axis, precision_square, color='blue', linestyle='--', marker='o')
	plt.savefig(filename)
	plt.show()

# x=resolução, y=precisão
# x=resolucao, y=n_cells
# x=n_cells, y=precisão