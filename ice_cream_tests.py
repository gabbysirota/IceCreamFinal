import unittest
from icecream import *

class testingDataGrab(unittest.TestCase):
	def test_one(self):
		ratings = rating_sort()
		self.assertEqual(len(ratings), 20)
		self.assertTrue(type(ratings[0])==str)
	def test_two(self):
		distances = distance_sort()
		self.assertEqual(len(distances), 20)
		self.assertTrue(type(distances[0])==str)
	def test_three(self):
		pass

# class testingDataStore(unittest.TestCase)

# class testingDataProcess(unittest.TestCase)

unittest.main()