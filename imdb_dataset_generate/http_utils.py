# -*- coding: utf-8 -*-

import requests
import urllib
import config

'''
given a URL for a web page (either http or https), get the HTML
content of that page
(for example, for url: https://www.google.co.in, this method will
return a string representing the HTML of the google home page)
'''
def get_html_from_url(url) :
	return urllib.urlopen(url).read()

'''
Uses the IMDB search API (description can be found : http://imdb.wemakesites.net/)
Takes in a search string (expected to be a movie name), and returns the results
as per what the search feature in the IMDB website (http://www.imdb.com/) does.
For sample result, look at "./test.json" file
'''
def imdb_search(search_string) :
	request_url = config.IMDB_SEARCH_API + '?api_key=' + config.IMDB_SEARCH_API_KEY + '&q=' + search_string
	print('\t' + request_url)
	r = requests.get(request_url)
	if r.status_code == 200 :
		print('\tsearch : request successfull')
		return r.json()
	print('\tsearch : request unsuccessfull : request code : ' + str(r.status_code))
