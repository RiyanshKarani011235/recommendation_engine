import requests
import ast
import json
import urllib
import re

api = 'http://imdb.wemakesites.net/api/search'
api_key = '57f7d535-df39-4028-9a33-c390bf2bbca1'
dataset_path = './data/ml-100k/u.item'

def crawl(movie_names_array) :

	def search(search_string) :
		request_url = api + '?api_key=' + api_key + '&q=' + search_string
		r = requests.get(request_url)
		if r.status_code == 200 : 
			print('\tsearch : request successfull')
			return r.json()
		print('\tsearch : request unsuccessfull : request code : ' + str(r.status_code))

	def get_html_from_url(url) : 
		return urllib.urlopen(url).read()

	def get_name_from_title(title) : 
		# title format : name (date)
		# return just name, with no spaces in the start and the end
		regex = r'[(][0-9]{4}[)]'
		match = re.search(regex, title)
		if match != None : 
			name = title[:match.start()]

			# remove spaces from start and end
			name = strip_spaces(name)

			# convert name to lower case
			return name.lower()

		print('get_name_from_title : no match')
		return None

	def strip_spaces(string) : 
		# removes spaces from start and end

		# remove extra spaces / tabs from the start
		i = 0
		while re.search(r'[ \t]', string[i]) :
			i += 1
		string = string[i:]

		# remove extra spaces / tabs from the end
		i = len(string) - 1
		while re.search(r'[ \t]', string[i]) :
			i -= 1

		return string[:i+1]

	def get_date_from_title(title) : 
		# title format : name (date)
		# return just date, with no spaces in the start and the end
		match = re.search(r'[(][0-9]{4}[)]', title)
		if match != None : 
			return title[match.start()+1: match.end()-1]

		print('get_date_from_title : no match')

	def get_movie_date_from_html(html) : 
		
		def return_none() : 
			print('\tget_movie_date_from_html : no match')
			return

		def validate_match(match_object) : 
			if match_object == None : 
				return_none()

		match = re.search(r'<span id="titleYear">.*?</span>', html)
		validate_match(match)

		string =  match.group(0)
		match = re.search(r'<span id="titleYear">', string)
		validate_match(match)

		string = string[match.end()+1:]
		match_object_start = -1
		for element in re.finditer(r'</span>', string) : 
			match_object_start = element.start()
		if match_object_start == -1 : 
			return_none()
		string = string[:match_object_start-1]

		match = re.search(r'<a href=".*?>', string)
		validate_match(match)
		string = string[match.end():]

		match = re.search(r'</a>', string)
		validate_match(match)
		string = string[:match.start()]

		return string

	for search_string in movie_names_array : 
		print('searching for ' + search_string)

		res = search(search_string)
		correct_responses = []

		if res != None :
			# parse unicode string into ascii string
			res = str(res)
			res = res.replace('u\'', '\'')
			res = dict(ast.literal_eval(res))

			# parse JSON to convert to python object
			titles = res['data']['results']['titles']

			# get URL's for correct titles
			for title in titles : 
				t = strip_spaces(title['title']).lower()
				if get_name_from_title(search_string) == t :
					correct_responses.append((search_string, title))

		# got all movies that are contextually valid
		# check move dates with that on the webpage
		# so as to filter movies with same names but with different dates
		correct_responses_ = []
		for element in correct_responses : 
			url = element[1]['url']
			print('\tfetching ' + url)
			html = get_html_from_url(url).replace('\n', '')

			# check dates for the corresponding movies
			if get_movie_date_from_html(html) == get_date_from_title(search_string) : 
				correct_responses_.append((search_string, html))

		correct_responses = correct_responses_
		print(correct_responses)

		#TODO: 
		# do something with html, and store the required data 
		# directors, actors, ...

		# append this data to element

		raise SystemExit(0)

def generate_dataset(filename) : 
	data = ''
	with open(filename, 'r') as f : 
		data = f.read()

	movie_names_array = []
	for line in data.split('\n') : 
		if line != '' :
			movie_names_array.append(line.split('|')[1])

	return movie_names_array

crawl(generate_dataset(dataset_path))