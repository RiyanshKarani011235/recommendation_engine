dataset_path = './data/ml-100k/u.item'

def parse_dataset() : 
	data = ''
	with open(dataset_path, 'r') as f : 
		data = f.read()

	movie_names_array = []
	for line in data.split('\n') : 
		if line != '' :
			movie_names_array.append(line.split('|')[1])

	return movie_names_array