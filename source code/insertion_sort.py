__author__ = 'Huy Vu'
'python implementation for insertion sort algorithm'
'use for sorting the data structure of the application'

def insertion_sort(array):
	for mark in range(1, len(array)):
		i = mark - 1
		tmp = array[mark]
		while i >= 0 and array[i] > tmp:
			array[i + 1] = array[i]
			i -= 1
		array[i + 1] = tmp
