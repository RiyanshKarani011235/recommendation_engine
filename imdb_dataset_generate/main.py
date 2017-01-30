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

saved_data_file_url = './data/data.txt'

def crawl(movie_names_array) :

	for i in range(len(movie_names_array)) : 
		search_string = movie_names_array[i]

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

		data_array = []
		for element in correct_responses : 
			html = element[1]

			country = imdb_movie_page_html_parse_utils.get_country_from_html(html)
			if country == None : 
				country = 'None'
			director = imdb_movie_page_html_parse_utils.get_director_from_html(html)
			if director == None : 
				director = 'None'
			actors = imdb_movie_page_html_parse_utils.get_actors_from_html(html)
			if actors == None : 
				actors = []

			string = search_string + '||' + movie_release_dates_array[i] + '||'
			for element in movie_genres_array[i] : 
				string += element + '&&'
			string = string[:-2] + '||' + country + '||' + director + '||'
			for element in actors : 
				string += element + '&&'
			string = string[:-2] + '\n'

			with open(saved_data_file_url, 'a') as f : 
				f.write(string)

if __name__ == '__main__' : 
	movie_names_array, movie_release_dates_array, movie_genres_array = dataset_utils.parse_dataset()
	crawl(movie_names_array)