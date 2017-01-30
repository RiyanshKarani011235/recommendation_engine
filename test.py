import requests
import yaml
import ast
import json
import urllib

api = 'http://imdb.wemakesites.net/api/search'
api_key = '57f7d535-df39-4028-9a33-c390bf2bbca1'
movie_names_array = ['iron man']

def crawl(movie_names_array) :

	def search(search_string) :
		request_url = api + '?api_key=' + api_key + '&q=' + search_string
		print(request_url)
		r = requests.get(request_url)
		print(r)
		if r.status_code == 200 : 
			print('request successfull')
			return r.json()
		print('request code : ' + str(r.status_code))

	def get_html_from_url(url) : 
		return urllib.urlopen(url).read()

	search_string_response_pairs = []
	return_array = []

	for search_string in movie_names_array : 
		res = search(search_string)
		if res == None :
			print('request unsuccessfull for movie : ' + search_string)
		else : 
			# parse unicode string into ascii string
			res = str(res)
			res = res.replace('u\'', '\'')
			res = dict(ast.literal_eval(res))

			# parse JSON to convert to python object
			titles = res['data']['results']['titles']

			# get URL's for correct titles
			for title in titles : 
				t = title['title'].lower() 
				if t == search_string : 
					search_string_response_pairs.append((search_string, title))

	# got all movies that are contextually valid
	for element in search_string_response_pairs : 
		url = element[1]['url']
		html = get_html_from_url(url)

		#TODO: 
		# do something with html, and store the required data 
		# directors, actors, ...

		# append this data to element

def generate_dataset(filename) : 
	data = ''
	with open(filename, 'r') as f : 
		data = f.read()

	movie_names = []
	for line in data.split('\n') : 
		print('line : ' + line)
		print(line.split('|')[1])
		movie_names.append(line.split('|')[1])

	print(movie_names)

generate_dataset('./dataset.txt')

# crawl(movie_names_array)