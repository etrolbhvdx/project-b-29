from unittest.mock import patch
from django.test import TestCase, RequestFactory
from .models import Message, Offering, Transfer
from django.http import HttpResponseRedirect
from views import transfer, search

# Create your tests here.
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
        #print(msgs)
        self.assertEqual(len(msgs), 1)

    #returning 404, unsure why
    # def test_seas_search(self):
    #     response = self.client.post('home/seas/search', {'search': 'APMA'})
    #     offerings = Offering.objects.all()
    #     self.assertEqual(response.status_code, 302)
    #     self.assertGreater(len(offerings), 0)
#
# class TransferTest(TestCase):
#     def test_transfer_function(self):
#         # Test case 1: Test transfer with valid index
#         request = self.factory.post('/', {'transfer': '1'})
#         response = transfer(request)
#         self.assertIsInstance(response, HttpResponseRedirect)
#         self.assertEqual(response.url, 'equivalencies')
#         self.assertEqual(Transfer.objects.count(), 1)
#
#         transfer_obj = Transfer.objects.first()
#         self.assertEqual(transfer_obj.transferClass, 'TRANS')
#         self.assertEqual(transfer_obj.title, 'Sample Transfer')
#         self.assertEqual(transfer_obj.transferCredits, '3')
#         self.assertEqual(transfer_obj.UVAClass, 'UVA101')
#         self.assertEqual(transfer_obj.UVACredits, '3')
#
#         # Test case 2: Test transfer with invalid index
#         request = self.factory.post('/', {'transfer': '10'})
#         response = transfer(request)
#         self.assertIsInstance(response, HttpResponseRedirect)
#         self.assertEqual(response.url, 'equivalencies')
#         self.assertEqual(Transfer.objects.count(), 0)
#
#         # Test case 3: Test transfer with empty index
#         request = self.factory.post('/', {'transfer': ''})
#         response = transfer(request)
#         self.assertIsInstance(response, HttpResponseRedirect)
#         self.assertEqual(response.url, 'equivalencies')
#         self.assertEqual(Transfer.objects.count(), 0)
#
#         def test_search_function(self, mock_get):
#             # Mock API response
#             api_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232'
#             mock_get.return_value.json.return_value = [{
#                 'subject': 'TEST',
#                 'catalog_nbr': '101',
#                 'class_section': '01',
#                 'descr': 'Test Course',
#                 'meetings': [
#                     {
#                         'days': 'MWF',
#                         'start_time': '08:00:00',
#                         'end_time': '08:50:00'
#                     }
#                 ],
#                 'enrollment_available': 5
#             }]
#
#             # Test case 1: Test search with a valid subject
#             request = self.factory.post('/', {'search': 'TEST'})
#             response = search(request)
#             self.assertIsInstance(response, HttpResponseRedirect)
#             self.assertEqual(response.url, 'results')
#             self.assertEqual(Offering.objects.count(), 1)
#
#             offering_obj = Offering.objects.first()
#             self.assertEqual(offering_obj.section, 'TEST 101-01')
#             self.assertEqual(offering_obj.name, 'Test Course')
#             self.assertEqual(offering_obj.day, 'MWF 08:00-08:50')
#             self.assertEqual(offering_obj.enrollment, '5')
#             self.assertEqual(offering_obj.if_full, False)  # Assuming isfull() returns a boolean
#
#             # Test case 2: Test search with an empty subject
#             request = self.factory.post('/', {'search': ''})
#             response = search(request)
#             self.assertIsInstance(response, HttpResponseRedirect)
#             self.assertEqual(response.url, 'results')
#             self.assertEqual(Offering.objects.count(), 0)

# class TestSearch(TestCase):
#     def test_search_function(self, mock_get):
#         # Mock API response
#         api_url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232'
#         mock_get.return_value.json.return_value = [{
#             'subject': 'TEST',
#             'catalog_nbr': '101',
#             'class_section': '01',
#             'descr': 'Test Course',
#             'meetings': [
#                 {
#                     'days': 'MWF',
#                     'start_time': '08:00:00',
#                     'end_time': '08:50:00'
#                 }
#             ],
#             'enrollment_available': 5
#         }]
#
#         # Test case 1: Test search with a valid subject
#         request = self.factory.post('/', {'search': 'TEST'})
#         response = search(request)
#         self.assertIsInstance(response, HttpResponseRedirect)
#         self.assertEqual(response.url, 'results')
#         self.assertEqual(Offering.objects.count(), 1)
#
#         offering_obj = Offering.objects.first()
#         self.assertEqual(offering_obj.section, 'TEST 101-01')
#         self.assertEqual(offering_obj.name, 'Test Course')
#         self.assertEqual(offering_obj.day, 'MWF 08:00-08:50')
#         self.assertEqual(offering_obj.enrollment, '5')
#         self.assertEqual(offering_obj.if_full, False)  # Assuming isfull() returns a boolean
#
#         # Test case 2: Test search with an empty subject
#         request = self.factory.post('/', {'search': ''})
#         response = search(request)
#         self.assertIsInstance(response, HttpResponseRedirect)
#         self.assertEqual(response.url, 'results')
#         self.assertEqual(Offering.objects.count(), 0)




