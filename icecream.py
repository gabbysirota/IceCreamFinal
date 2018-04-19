import sqlite3
import csv
import json
import secrets
from secrets import APIKey
import requests
from bs4 import BeautifulSoup
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go

API_CACHE = 'api_cache_file.json'
try:
	cache_file = open(API_CACHE, 'r')
	cache_contents = cache_file.read()
	API_CACHE_DICT = json.loads(cache_contents)
	cache_file.close()

except:
	API_CACHE_DICT = {}

SCRAPING_CACHE = 'scrape_cache_file.json'
try:
	cache_file1 = open(SCRAPING_CACHE, 'r')
	cache_contents1 = cache_file1.read()
	SCRAPE_CACHE_DICTION = json.loads(cache_contents1)
	cache_file1.close()

except:
	SCRAPE_CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
	alphabetized_keys = sorted(params.keys())
	res = []
	for k in alphabetized_keys:
		res.append("{}-{}".format(k, params[k]))
	return baseurl + "_".join(res)


def make_request_using_cache(baseurl, params={}, auth=None):
	unique_ident = params_unique_combination(baseurl,params)

	if unique_ident in SCRAPE_CACHE_DICTION:
		#print("Getting cached data...")
		return SCRAPE_CACHE_DICTION[unique_ident]

	else:
		#print("Making a request for new data...")
		resp = requests.get(baseurl, params, auth=auth)
		SCRAPE_CACHE_DICTION[unique_ident] = resp.text
		dumped_json_cache = json.dumps(SCRAPE_CACHE_DICTION)
		fw = open(SCRAPING_CACHE,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return SCRAPE_CACHE_DICTION[unique_ident]


def get_from_cache(location):
	baseurl = "https://api.yelp.com/v3/businesses/search"
	params_diction = {}
	params_diction["term"] = "ice cream"
	params_diction["location"] = location

	if location in API_CACHE_DICT:
		print("Getting cached data...")
		return API_CACHE_DICT[location]
	else:
		print("Making a request for new data...")

		response = requests.get('https://api.yelp.com/v3/businesses/search', headers={'Authorization': 'Bearer %s' % APIKey}, params=params_diction)
		API_CACHE_DICT[location] = json.loads(response.text)
		dumped_json_cache = json.dumps(API_CACHE_DICT)
		fw = open(API_CACHE,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		print(API_CACHE_DICT[location])
		return API_CACHE_DICT[location]

class store:
	def __init__(self, name, address, review):
		self.name = name
		self.address = address
		self.review = review
	def __str__(self):
		return "Someone said: {} about {}".format(self.review, self.name)

# def scrape(location, storename):
# 	start_number = 0
# 	for x in range(0, 100, 10):
# 		page_text = make_request_using_cache("https://www.yelp.com/search", params = {"find_loc" : "ann arbor, mi", "find_desc":"ice cream"})
# 		page_soup = BeautifulSoup(page_text, 'html.parser')
# 		print(page_soup)
		# all_store_container = page_soup.find_all("ul", class_="ylist ylist-bordered search-results js-search-results yloca-pills-blue yloca-wrapper-grey")
		# store_container = all_store_container[1]
		# store_lists = store_container.find_all("li", class_="regular-search-result")
		# # print(store_lists[0].prettify())
		# store_list_names = []
		# # for store in store_lists:
		# # 	first = store.find("div", {"data-biz-id" : "W4WNypFs--aQfpG0V5gsxQ"})
		# # 	second = first.find("div", class_="biz-listing-large")
		# # 	second_one = second.find("div", class_="media-block media-block--18")
		# # 	print(second.prettify())
		# # 	third = second_one.find("div", class_="media-attributes")
		# # 	fourth = third.find("div", class_="media-block media-block--12")
		# # 	fifth = fourth.find("div", class_="media-story")
		# # 	sixth = fifth.find("h3", class_="search-result-title")
		# # 	seven = sixth.find("a", class_="biz-name jas-analytics-click")
		# # 	store_name = seven.find("span").text
		# # 	store_name = store.find("h3", class_= "search-result-title").text
		# for store in store_lists:
		# 	first = store.find("div", class_="search-result natural-search-result scrollable-photos-search-result")
		# 	second = first.find("div", class_="biz-listing-large")
		# 	second_one = second.find("div", class_="media-block media-block--18")
		# 	third = second_one.find("div", class_="media-story")
		# 	fourth = third.find("div", class_="biz-attributes")
		# 	fifth = fourth.find("div", class_="main-attributes")
		# 	sixth = fifth.find("h3", class_="search-result-title")
		# 	seven = sixth.find("span", class_="indexed-biz-name")
		# 	eight = seven.find("a")
		# 	store_name = eight.find("span").text
		# 	print(store_name)
		# 	# sixth = fifth.find("h3", class_="search-result-title")
		# 	# seven = sixth.find("a", class_="biz-name jas-analytics-click")
		# 	# store_name = seven.find("span").text
		# 	# store_name = store.find("h3", class_= "search-result-title").text
		# 	if store_name == storename:
		# 		url = eight["href"]
		# 		second_page = make_request_using_cache("https://www.yelp.com/{}".format(url))
		# 		print("did it")
		# 		soup = BeautifulSoup(second_page, "html.parser")
		# 		container = soup.find("div", class_= "map-box-address")
		# 		store_address = container.find("address").text
		# 		return store_address







# inp = input('Enter a location: ')
# x = get_from_cache(inp)
# #print(len(x['businesses']))
#
# r = get_from_cache("ann arbor, mi")
# s = json.dumps(r)
# page_soup = BeautifulSoup(s, 'html.parser')
# print(page_soup)
# page_text = get_from_cache(location)
# page_soup = BeautifulSoup(page_text, 'html.parser')
# print (page_soup)


# 	data = get_from_cache(location)
# 	soup = BeautifulSoup(data, "html.parser")
# 	return soup
# print (get_store_info("ann arbor, mi"))

DBNAME = 'icecream.db'
#BARSCSV = 'flavors_of_cacao_cleaned.csv'
cache = 'cache_file_name.json'


def init_db():
	try:
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
	except Error as e:
		print(e)

	statement = '''
		DROP TABLE IF EXISTS 'IceCream';
	'''
	statement2 = "DROP TABLE IF EXISTS 'Stores';"
	cur.execute(statement)
	cur.execute(statement2)
	conn.commit()


	statement = '''
		CREATE TABLE 'IceCream' (
			'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
			'Name' TEXT,
			'Distance' INTEGER,
			'Rating' INTEGER,
			'ReviewCount' INTEGER
		);
	'''
	statement2 = '''
	CREATE TABLE 'Stores' (
		'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'Name' TEXT,
		'Address' TEXT,
		'StoreId' INTEGER,
		'SearchLocation' TEXT
		);'''

	cur.execute(statement)
	cur.execute(statement2)
	conn.commit()
	conn.close()


def insert_icecream(data):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	for count in data['businesses']:
		insertion = (None, count['name'], count['distance'], count['rating'], count['review_count'])
		statement = 'INSERT INTO "IceCream" '
		statement += 'VALUES (?, ?, ?, ?, ?)'
		cur.execute(statement, insertion)
		conn.commit()
	conn.close()

def insert_scrape_icecream(data):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	insertion = (None, data[0], data[1], data[2], data[3])
	statement = 'INSERT INTO "Stores" '
	statement += 'VALUES (?, ?, ?, ?, ?)'
	cur.execute(statement, insertion)
	conn.commit()
	conn.close()

def scrape(location, storename):
	result = make_request_using_cache("https://www.yelp.com/search", params = {"find_loc" : location, "find_desc":"ice cream"})
	soup = BeautifulSoup(result, 'html.parser')
	## content = soup.find(class_='main-content-wrap main-content-wrap--full')
	search_results = soup.find_all('address')
	name_results = soup.find_all('h3', class_='search-result-title')
	count = 1
	address_dict = {}
	for name in name_results:
		x = name.text.strip()
		if '.' in x:
			address_dict[x] = search_results[count].text.strip()
			count += 1
	# for address in search_results:
	# 	print(address.text.strip())
	for item in list(address_dict.keys()):
		if storename in item:
			save_address = address_dict[item]
	all_data = (storename, save_address, "store_id", location)
	insert_scrape_icecream(all_data)
	return "done"

def rating_sort():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	statement = 'SELECT Name, Rating FROM IceCream ORDER BY Rating DESC'
	y = cur.execute(statement).fetchall()
	return [store[0] for store in y]

def distance_sort():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	statement = 'SELECT Name, Distance FROM IceCream ORDER BY Distance ASC'
	y = cur.execute(statement).fetchall()
	return [store[0] for store in y]

def generate_graphs():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	y = cur.execute('SELECT Name, Distance FROM IceCream').fetchall()
	stores = [store[0] for store in y]
	distances = [d[1] for d in y]
	data = [go.Bar(
            x=stores,
            y=distances
    )]
	py.plot(data, filename='Distances')

	x = cur.execute('SELECT Name, ReviewCount FROM IceCream').fetchall()
	stores1 = [store[0] for store in x]
	review_counts = [r[1] for r in x]
	data1 = [go.Bar(
            x=stores1,
            y=review_counts
    )]
	py.plot(data1, filename='Review Counts')

	z = cur.execute('SELECT Rating FROM IceCream').fetchall()
	review_d = {}
	for review in z:
		if review not in review_d:
			review_d[review] = 0
		review_d[review] += 1
	rating_values = list(review_d.keys())
	ratings = [review_d[label] for label in rating_values]

	labels = rating_values
	values = ratings

	trace = go.Pie(labels=labels, values=values)

	py.plot([trace], filename='Rating Distribution')

	a = cur.execute('SELECT Name, Rating FROM IceCream ORDER BY Rating DESC').fetchone()
	b = cur.execute('SELECT Name, ReviewCount FROM IceCream ORDER BY ReviewCount DESC').fetchone()
	print(a, b)
	top_rated = a[0]
	top_reviewed = b[0]
	top_rated_info = cur.execute('SELECT Name, Rating, ReviewCount FROM IceCream WHERE Name = "%s"' %top_rated).fetchone()
	top_reviewed_info = cur.execute('SELECT Name, Rating, ReviewCount FROM IceCream WHERE Name = "%s"' %top_reviewed).fetchone()
	trace1 = go.Bar(x=['Rating', 'Review Count'],y=[top_rated_info[1], top_rated_info[1]],name=top_rated_info[0])
	trace2 = go.Bar(x=['Rating', 'Review Count'],y=[top_reviewed_info[1], top_reviewed_info[1]], name=top_reviewed_info[0])
	data = [trace1, trace2]
	layout = go.Layout(barmode='group')
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='Top Rated vs Top Reviewed')

def interaction():
	inp = ''
	while inp != 'exit':
		inp = input('Enter a location (sample format: ann arbor, mi): ')
		if inp == 'exit':
			print('exiting...')
			exit()
		data = get_from_cache(inp)
		init_db()
		insert_icecream(data)
		results_inp = ''
		while results_inp != 'exit' or inp != 'new location':
			results_inp = input("""How would you like to view your results:
				rating
				distance
				view all graphs
				""")
			if results_inp == 'exit':
				print('exiting...')
				exit()
			elif results_inp == 'new location':
				break
			if results_inp == 'rating':
				print("""Results Ordered By Rating
--------------------------------------------------------

					""")
				count = 0
				for store in rating_sort():
					count += 1
					number = '{}: '.format(count)
					print(number, store)
				store_inp = input('Type a store name exactly as it appears: ')
				info = scrape(inp, store_inp)
				print(info)
			elif results_inp == 'distance':
				print("""Results Ordered By Distance
--------------------------------------------------------

					""")
				count = 0
				for store in distance_sort():
					count += 1
					number = '{}: '.format(count)
					print(number, store)
			elif results_inp == 'view all graphs':
				generate_graphs()
			else:
				print('Please enter a valid command')

#interaction()
get_address("https://www.yelp.com/search?cflt=icecream&find_loc=Ann+Arbor%2C+MI")
