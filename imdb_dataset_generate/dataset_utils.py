import config

genres_list = ['unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

def parse_dataset() : 
	data = ''
	with open(config.ITEMS_DATASET_PATH, 'r') as f : 
		data = f.read()

	movie_names_array = []
	movie_release_date_array = []
	movie_genres_array = []
	movie_urls_array = []

	for line in data.split('\n') : 
		if line != '' :
			movie_names_array.append(line.split('|')[1])
			movie_release_date_array.append(line.split('|')[2])
			movie_urls_array.append(line.split('|')[4])
			genres = line.split('|')[5:]
			genres_ = []
			for i in range(len(genres)) : 
				if genres[i] == '1' : 
					genres_.append(genres_list[i])
			movie_genres_array.append(genres_)

	return movie_names_array, movie_release_date_array, movie_genres_array, movie_urls_array