import re

def validate_match(match_object) : 
	if match_object == None : 
		return False
	return True

def return_none() : 
	print('\tget_movie_date_from_html : no match')
	return

def get_movie_date_from_html(html) : 

	match = re.search(r'<span id="titleYear">.*?</span>', html)
	if not validate_match(match) : 
		return None

	string =  match.group(0)
	match = re.search(r'<span id="titleYear">', string)
	if not validate_match(match) : 
		return None

	string = string[match.end()+1:]
	match_object_start = -1
	for element in re.finditer(r'</span>', string) : 
		match_object_start = element.start()
	if match_object_start == -1 : 
		return_none()
	string = string[:match_object_start-1]

	match = re.search(r'<a href=".*?>', string)
	if not validate_match(match) : 
		return None
	string = string[match.end():]

	match = re.search(r'</a>', string)
	if not validate_match(match) : 
		return None
	string = string[:match.start()]

	return string

def get_country_from_html(html) : 
	'''
	<div class="txt-block">
    	<h4 class="inline">Country:</h4>
        <a href="/search/title?country_of_origin=us&amp;ref_=tt_dt_dt" itemprop="url">USA</a>
    </div>
	'''
	match = re.search(r'<div class="txt-block">[ ]*?<h4 class="inline">Country:</h4>.*?</a>', html)
	if not validate_match(match) : 
		return None

	string = html[match.start():match.end()]
	match = re.search(r'</a>', string)
	if not validate_match(match) : 
		return None

	string = string[:match.start()]

	match = re.search(r'<a href=".*?>', string)
	if not validate_match : 
		return None

	string = string[match.end():]

	return string

def get_director_from_html(html) : 
	'''
	<div class="credit_summary_item">
        <h4 class="inline">Director:</h4>
            <span itemprop="director" itemscope="" itemtype="http://schema.org/Person">
			<a href="/name/nm0269463?ref_=tt_ov_dr" itemprop="url"><span class="itemprop" itemprop="name">Jon Favreau</span></a>            </span>
    </div>
	'''
	match = re.search(r'<div class="credit_summary_item">[ ]*?<h4 class="inline">Director:</h4>.*?</div>', html)
	if not validate_match(match) : 
		return None

	string = html[match.start():match.end()]

	match = re.search(r'<a href=".*?</a>', string)
	if not validate_match(match) : 
		return None

	string = string[match.start():match.end()]

	match = re.search(r'</span>', string)
	if not validate_match(match) : 
		return None

	string = string[:match.start()]

	match = re.search(r'<span.*?>', string)
	if not validate_match(match) : 
		return None

	string = string[match.end():]

	return string

def get_actors_from_html(html) : 
	actors_array = []

	match = re.search(r'<div class="credit_summary_item">[ ]*?<h4 class="inline">Stars:</h4>.*?</div>', html)
	if not validate_match(match) : 
		return None

	string = html[match.start():match.end()]

	for string_ in re.findall(r'<a href=".*?</a>', string) : 
		match = re.search(r'</span>', string_)
		if validate_match(match) : 
			string_ = string_[:match.start()]

			match = re.search(r'<span.*?>', string_)
			if validate_match(match) : 
				string_ = string_[match.end():]
				actors_array.append(string_)

	return actors_array


