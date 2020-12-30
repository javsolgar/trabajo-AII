import string
import random

from django.test.client import MULTIPART_CONTENT
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client = None

    def test_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_ok(self):
        answers = {
            'username': 'admin',
            'password1': 'admin'
        }
        response = self.client.post('/accounts/login/', answers)
        self.assertEqual(response.status_code, 200)

    def test_registro(self):
        response = self.client.get('/registro/')
        self.assertEqual(response.status_code, 200)

    def test_registro_ok(self):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        answers = {
            'username': username,
            'password1': '52108883A',
            'password2': '52108883A'
        }
        response = self.client.post('/registro/', answers)
        self.assertEqual(response.status_code, 200)
