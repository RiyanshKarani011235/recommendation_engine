import config

def parse_dataset() : 
	data = ''
	with open(config.ITEMS_DATASET_PATH, 'r') as f : 
		data = f.read()

	movie_names_array = []
	for line in data.split('\n') : 
		if line != '' :
			movie_names_array.append(line.split('|')[1])

	return movie_names_array