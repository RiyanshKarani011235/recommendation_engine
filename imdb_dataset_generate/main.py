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

use_new_implementation = True

def update_start_movie_number(number) : 
	start_movie_number = ''
	lines_array = []
	with open(saved_data_file_url, 'r') as f : 
		lines_array = f.read().split('\n')
		try : 
			start_movie_number = int(lines_array[0]) + 1
		except Exception as e : 
			pass

	if start_movie_number == '' : 
		# start_movie_number not present
		new_lines_array = [str(number)]
		new_lines_array.extend(lines_array)
		lines_array = new_lines_array
	else : 
		# start_movie_number present, so replace
		lines_array[0] = str(number)

	# write the file again
	with open(saved_data_file_url, 'w') as f : 
		for i in range(len(lines_array)) : 
			line  = lines_array[i]
			if i == 0 : 
				f.write(line)
			else : 
				f.write('\n' + line)

def increment_start_movie_number() : 
	start_movie_number = 0
	with open(saved_data_file_url, 'r') as f : 
		try : 
			start_movie_number = int(f.read().split('\n')[0]) + 1
		except Exception as e : 
			start_movie_number += 1

	update_start_movie_number(start_movie_number)

def crawl(movie_names_array) :

	def nothing_found(search_string, message) : 
		print(search_string + ' : ' + message)
		string = search_string + '||\n'
		with open(saved_data_file_url, 'a') as f : 
			f.write(string)

	# find the start movie number
	start_movie_number = 0
	with open(saved_data_file_url, 'r') as f : 
		try :
			start_movie_number = int(f.read().split('\n')[0]) + 1
		except Exception as e : 
			pass

	print('starting from movie number : ' + str(start_movie_number))

	for i in range(start_movie_number, len(movie_names_array)) : 

		try : 
			search_string = movie_names_array[i]

			# strip date from the name, and search using just the name
			array_ = search_string.split('(')[:-1]
			search_string_ = ''
			for element in array_ : 
				search_string_ += element + '('
			search_string_ = string_utils.strip_spaces(search_string_[:-1]).lower()

			print('searching for ' + search_string_)
			correct_responses = []


			res = http_utils.imdb_search(search_string_)
			
			if res != None :
				# parse unicode string into ascii string
				res = str(res)
				res = res.replace('u\'', '\'')
				res = res.replace('\n', '')
				res = dict(ast.literal_eval(res))

				print(res)

				# parse JSON to convert to python object
				try : 
					titles = res['data']['results']['titles']
				except : 
					nothing_found(search_string, '\tno results')
					increment_start_movie_number()
					continue
				
				# get URL's for correct titles
				for title in titles : 
					t = string_utils.strip_spaces(title['title']).lower()
					if string_utils.get_name_from_title(search_string) == t :
						correct_responses.append((search_string, title))

			else :
				nothing_found(search_string, '\tresponse is None')
				increment_start_movie_number()
				continue

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
				movie_date = imdb_movie_page_html_parse_utils.get_movie_date_from_html(html)
				print(movie_date)
				if movie_date == string_utils.get_date_from_title(search_string) : 
					correct_responses_.append((search_string, html))

					# greedy
					break

			correct_responses = correct_responses_

			if len(correct_responses) == 0 : 
				nothing_found(search_string, '\t0 correct responses')
				increment_start_movie_number()
				continue

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

		except Exception as e : 

			string = search_string + '||'
			with open(saved_data_file_url, 'a') as f : 
					f.write(string)

		increment_start_movie_number()


if __name__ == '__main__' : 
	movie_names_array, movie_release_dates_array, movie_genres_array, movie_urls_array = dataset_utils.parse_dataset()
	crawl(movie_names_array)
