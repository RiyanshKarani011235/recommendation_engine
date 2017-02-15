# -*- coding: utf-8 -*-
saved_data_file_url = './data/data.txt'

with open(saved_data_file_url, 'r') as f :
	num = 0
	total = 0
	for line in f.read().split('\n')[1:-1] :
		print(line.split('||'))
		if not line.split('||')[1] == '' :
			num += 1
		total += 1
	print(num)
	print(total)
