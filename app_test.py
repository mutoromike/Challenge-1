import unittest
from flask import Flask
from app import views

class FirstTest(unittest.TestCase):

    def test_details(self):
        self.assertEqual(status_code, 200)

if __name__ == '__main__':
    unittest.main()