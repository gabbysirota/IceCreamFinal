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
	def __init__(self, name, address):
		self.name = name
		self.address = address
	def __str__(self):
		return "{} is located at {}".format(self.name, self.address)

store_instances = []

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
	start_number = 0
	for x in range(0, 20, 10):
		result = make_request_using_cache("https://www.yelp.com/search", params = {"find_loc" : location, "find_desc":"ice cream", "start": x})
		soup = BeautifulSoup(result, 'html.parser')
		## content = soup.find(class_='main-content-wrap main-content-wrap--full')
		search_results = soup.find_all('address')
		name_results = soup.find_all('h3', class_='search-result-title')
		for each in name_results:
			y = each.text.strip()
			if storename in y:
				span = each.find('span', class_='indexed-biz-name')
				if span:
					url = span.find('a')['href']
					second_page = requests.get("https://www.yelp.com/{}".format(url)).text
					#second_page = make_request_using_cache("https://www.yelp.com/{}".format(url))
					soup = BeautifulSoup(second_page, "html.parser")
					new_soup = soup.find_all('address')[0]
					clean = new_soup.text.strip()
					store_instances_names = [s.name for s in store_instances]
					new_store = store(storename, clean)
					if new_store.name not in store_instances_names:
						store_instances.append(new_store)
					all_data = (new_store.name, new_store.address, "store_id", location)
					insert_scrape_icecream(all_data)
					return clean

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
				store_inp = input('Type a store name exactly as it appears: ')
				info = scrape(inp, store_inp)
				print(info)
			elif results_inp == 'view all graphs':
				generate_graphs()
			else:
				print('Please enter a valid command')

if __name__ == "__main__":
	interaction()
