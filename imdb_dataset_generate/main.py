'''
Features to use from IMDB database:
	1.Actor
	2.Actress
	3.Country 
	4.Director
	5.keywords
	6.Producer
	7.Production Company
	8.Production Designer
'''

import ast
import json
import re

import dataset_utils
import http_utils
import imdb_movie_page_html_parse_utils
import string_utils

def crawl(movie_names_array) :

	for search_string in movie_names_array : 
		print('searching for ' + search_string)

		res = http_utils.imdb_search(search_string)
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
				t = string_utils.strip_spaces(title['title']).lower()
				if string_utils.get_name_from_title(search_string) == t :
					correct_responses.append((search_string, title))

		# got all movies that are contextually valid
		# check move dates with that on the webpage
		# so as to filter movies with same names but with different dates
		correct_responses_ = []
		for element in correct_responses : 
			url = element[1]['url']
			print('\tfetching ' + url)
			# make all html in one line (for regex compatiblity)
			html = http_utils.get_html_from_url(url).replace('\n', '')

			# check dates for the corresponding movies
			if imdb_movie_page_html_parse_utils.get_movie_date_from_html(html) == string_utils.get_date_from_title(search_string) : 
				correct_responses_.append((search_string, html))

		correct_responses = correct_responses_

		#TODO: 
		# do something with html, and store the required data 
		# directors, actors, ...

		# append this data to element
		raise SystemExit(0)

if __name__ == '__main__' : 
	dataset = dataset_utils.parse_dataset()
	crawl(dataset)