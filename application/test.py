import os
import django
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client = None

    def test(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
