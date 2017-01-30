import re

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