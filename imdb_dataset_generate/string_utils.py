# -*- coding: utf-8 -*-

import re

'''
takes the following input "iron man (2008)"
(which is supposed to be the format of movie name string from the database)

returns the output "iron man"
'''
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

'''
takes a string such as "  hello world 	!	"
returns "hello world 	!"
'''
def strip_spaces(string) :
	# removes spaces from start and end

	if len(string) == 0 :
		return string
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

'''
takes the following input "iron man (2008)"
(which is supposed to be the format of movie name string from the database)

returns the output "2008" / None (None only if format is not as above)
'''
def get_date_from_title(title) :
	# title format : name (date)
	# return just date, with no spaces in the start and the end
	match = re.search(r'[(][0-9]{4}[)]', title)
	if match != None :
		return title[match.start()+1: match.end()-1]

	print('get_date_from_title : no match')
