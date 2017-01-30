import re

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