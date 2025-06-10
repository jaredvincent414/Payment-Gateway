# payments/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Payment

class PaymentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_payment(self):
        data = {
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "amount": 100.00
        }
        response = self.client.post('/api/v1/payments', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("payment_id", response.data)

    def test_retrieve_payment(self):
        payment = Payment.objects.create(
            customer_name="Jane Doe",
            customer_email="jane@example.com",
            amount=75.00
        )
        response = self.client.get(f'/api/v1/payments/{payment.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['payment']['customer_name'], "Jane Doe")
