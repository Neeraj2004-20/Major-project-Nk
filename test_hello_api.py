import unittest
import requests

class TestHelloAPI(unittest.TestCase):
    def test_hello(self):
        response = requests.get('http://localhost:8000/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Hello, world!')

if __name__ == '__main__':
    unittest.main()