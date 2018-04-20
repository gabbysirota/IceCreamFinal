import unittest
from icecream import *

class testingDataGrab(unittest.TestCase):
	def test_one(self):
		ratings = rating_sort()
		self.assertEqual(len(ratings), 20)
		self.assertTrue(type(ratings[0])==str)
		# ratings tests test we are getting 20 ice cream stores
		# each item in the list is a string (aka ice cream store name)
	def test_two(self):
		distances = distance_sort()
		self.assertEqual(len(distances), 20)
		self.assertTrue(type(distances[0])==str)
		# second 2 do the same thing but for distance
	def test_three(self):
		pass




# class testingDataStore(unittest.TestCase)

# class testingDataProcess(unittest.TestCase)

unittest.main()
