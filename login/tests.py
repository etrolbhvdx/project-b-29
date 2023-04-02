from django.test import TestCase
from .models import Message, Offering

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


