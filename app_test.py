import unittest
from flask import Flask
from app import views

class FirstTest(unittest.TestCase):

    def test_successful_create_new_user(self):
        result = {"mike":["mike@mike.com","123456"]}
        msg = views.create_new_user('mike', 'mike@mike.com', '123456')
        self.assertEqual(msg, result)
        
if __name__ == '__main__':
    unittest.main()