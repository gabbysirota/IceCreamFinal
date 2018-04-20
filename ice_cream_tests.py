import unittest
from icecream import *

class testingDataGrab(unittest.TestCase):
	def test_one(self):
		ratings = rating_sort()
		self.assertTrue(len(ratings) >= 10)
		self.assertTrue(type(ratings[0])==str)

	def test_two(self):
		distances = distance_sort()
		self.assertTrue(len(distances) >= 10)
		self.assertTrue(type(distances[0])==str)

	def test_three(self):
		data = get_from_cache('ann arbor, mi')
		self.assertTrue(type(data), dict)
		new_data = make_request_using_cache("https://www.yelp.com/search", params = {"find_loc" : "ann arbor, mi", "find_desc":"ice cream"})
		self.assertTrue(type(new_data), dict)

class testingDataStore(unittest.TestCase):
	def test_four(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		y = cur.execute('SELECT * FROM IceCream').fetchone()
		self.assertEqual(len(y), 5)
		self.assertEqual(type(y[2]), float)
		self.assertEqual(type(y[4]), int)


	def test_five(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		z = cur.execute('SELECT * FROM Stores').fetchone()
		self.assertEqual(len(z), 5)
		self.assertEqual(type(z[1]), str)

class testingDataProcess(unittest.TestCase):
	def test_six(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		ratings = rating_sort()
		a = cur.execute('SELECT Rating FROM IceCream WHERE Name = ?', (ratings[0],)).fetchone()
		b = cur.execute('SELECT Rating FROM IceCream WHERE Name = ?', (ratings[-1],)).fetchone()
		self.assertTrue(a > b)

	def test_seven(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		distances = distance_sort()
		a = cur.execute('SELECT Distance FROM IceCream WHERE Name = ?', (distances[0],)).fetchone()
		b = cur.execute('SELECT Distance FROM IceCream WHERE Name = ?', (distances[-1],)).fetchone()
		self.assertTrue(a < b)

	def test_eight(self):
		conn = sqlite3.connect(DBNAME)
		cur = conn.cursor()
		g = generate_graphs()
		self.assertTrue(len(g[0])==len(g[1]))
		self.assertEqual(len(g[2]), len(g[3]))

unittest.main()
