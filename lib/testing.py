import unittest
import transaction
from datetime import datetime
from app import application
from flask import jsonify
import json

active = True
isinsideallowlist = True
limit = 1000
merchant = 'Americanas'
amount = 50

payload = { "Transaction": { "merchant": "Americanas", "amount": 50, "time": "2019-06-16 14:40:52" }}
payload_overLimit = { "Transaction": { "merchant": "Americanas", "amount": 1001, "time": "2019-06-16 14:40:52" }}

last_transactions = [{
    "merchant": "Americanas",
    "amount": 100,
    "time": "2019-06-16 14:40:52"
  },
  {
    "merchant": "Americanas",
    "amount": 200,
    "time": "2019-06-16 14:40:52"
  },]

merchant_deny_list = ['Golpe Certo', 'Tudo Gratis']

time_transaction = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

t = transaction.Transaction(active, isinsideallowlist ,limit, \
merchant, amount,last_transactions, merchant_deny_list, time_transaction)

class FlaskTestCase(unittest.TestCase):
    def test_authorize_payload(self):
        tester = application.test_client(self)
        response = tester.post('/authorize', content_type='application/json', data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)

    def test_authorize_newlimit(self):
        tester = application.test_client(self)
        response = tester.post('/authorize', content_type='application/json', data=json.dumps(payload))
        self.assertEqual(json.loads(response.data)['newLimit'], 900)

    def test_authorize_approved(self):
        tester = application.test_client()
        response = tester.post('/authorize', content_type='application/json', data=json.dumps(payload))
        self.assertEqual(json.loads(response.data)['approved'], True)

    def test_authorize_blocked(self):
        tester = application.test_client()
        response = tester.post('/authorize', content_type='application/json', data=json.dumps(payload_overLimit))
        self.assertEqual(json.loads(response.data)['approved'], False)

    def test_authorize_deniedReasons(self):
        tester = application.test_client()
        response = tester.post('/authorize', content_type='application/json', data=json.dumps(payload_overLimit))
        self.assertIn(b'limitExceeded', json.loads(response.data)['deniedReasons'])

class TestTransactions(unittest.TestCase):

    def test_validateFields(self):
        self.assertTrue(t.validateFields())

    def test_getkWithinLimit(self):
        self.assertTrue(t.getkWithinLimit())

    def test_getActive(self):
        self.assertTrue(t.getActive())

    def test_getNewLimit(self):
        self.assertEqual(t.getNewLimit(), 950)

    def test_getFirstBelowPercent(self):
        self.assertTrue(t.getFirstBelowPercent())

    def test_checkLessTenMerchantRule(self):
        self.assertTrue(t.checkLessTenMerchantRule())

    def test_checkOutDenyList(self):
        self.assertTrue(t.checkOutDenyList())

    def test_checkLessThanFourInTwoMinutes(self):
        self.assertTrue(t.checkLessThanFourInTwoMinutes())

if __name__ == '__main__':
    unittest.main()
