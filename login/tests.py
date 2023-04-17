from unittest.mock import patch
from django.test import TestCase, RequestFactory
from .models import Message, Offering, Transfer
from django.http import HttpResponseRedirect



class SeasTestCase(TestCase):

    def test_seas_results(self):
        response = self.client.get('/home/seas/results')
        self.assertEqual(response.status_code, 200)

    def test_seas_approved(self):
        response = self.client.get('/home/seas/approved')
        self.assertEqual(response.status_code, 200)

    def test_seas_message_post(self):
        response = self.client.post(path='/home/seas/post')
        msgs = Message.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(msgs), 1)


