import requests
import urllib

# constants
IMDB_SEARCH_API = 'http://imdb.wemakesites.net/api/search'
IMDB_SEARCH_API_KEY = '57f7d535-df39-4028-9a33-c390bf2bbca1'

def imdb_search(search_string) :
	request_url = IMDB_SEARCH_API + '?api_key=' + IMDB_SEARCH_API_KEY + '&q=' + search_string
	r = requests.get(request_url)
	if r.status_code == 200 : 
		print('\tsearch : request successfull')
		return r.json()
	print('\tsearch : request unsuccessfull : request code : ' + str(r.status_code))

def get_html_from_url(url) : 
	return urllib.urlopen(url).read()