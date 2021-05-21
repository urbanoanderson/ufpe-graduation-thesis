#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True
from random import randint

class Measurement(object):
	def __init__(self, model):
		self.ta = model

def FilterGrid(grid_list, test_sample):
	subsets = [[] for x in range(len(test_sample.ta)+1)]
	print subsets
	for cell in grid_list:
		points = 0
		for i in range(len(cell.ta)):
			if cell.ta[i] == test_sample.ta[i]:
				points += 1
		print points
		(subsets[points]).append(cell)
	
	#for subset in subsets:
		#print len(subset)

	for subset in reversed(subsets):
		if(len(subset) > 0):
			return subset

if __name__ == "__main__":

	grid_list = []
	for i in range(3):
		grid_list.append(Measurement([1,1,1]))
	for i in range(3):
		grid_list.append(Measurement([2,2,2]))
	for i in range(3):
		grid_list.append(Measurement([3,3,3]))
	for i in range(3):
		grid_list.append(Measurement([4,4,4]))

	sample = Measurement([1,2,2])

	filtered_grid = FilterGrid(grid_list, sample)

	print len(filtered_grid)




# #É um subset pra cada quantidade de pontos (0,1,2,3)
# subsets = [[]]*(num_erbs+1) #vai gerar [[],[],[],[]] com 3 erbs
# for cell in grid_list:
# 	points = 0
# 	for i in range(len(cell.ta)):
# 		if cell.ta[i] == test_sample.ta[i]:
# 			points += 1 #cada acerto é 1 ponto
# 	print points #aqui tá calculando corretamente os pontos

# 	#aqui por algum motivo está inserindo em todos os subsets
# 	(subsets[points]).append(cell)

# #Depois disso retona o subset com mais pontos que nao esteja vazio
# #...