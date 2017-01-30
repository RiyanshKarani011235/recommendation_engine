import requests
import urllib
import config

def imdb_search(search_string) :
	request_url = config.IMDB_SEARCH_API + '?api_key=' + config.IMDB_SEARCH_API_KEY + '&q=' + search_string
	r = requests.get(request_url)
	if r.status_code == 200 : 
		print('\tsearch : request successfull')
		return r.json()
	print('\tsearch : request unsuccessfull : request code : ' + str(r.status_code))

def get_html_from_url(url) : 
	return urllib.urlopen(url).read()