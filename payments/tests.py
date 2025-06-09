from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Payment
from unittest.mock import patch

class PaymentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payment_data = {
            "customer_name": "Test User",
            "customer_email": "test@example.com",
            "amount": "100.00"
        }

    def test_create_payment(self):
        with patch('paypalrestsdk.Payment.create') as mock_create:
            mock_create.return_value = True
            
            with patch('paypalrestsdk.Payment.links') as mock_links:
                mock_links.__iter__.return_value = [
                    type('Link', (), {'rel': 'approval_url', 'href': 'http://test-url.com'})()
                ]
                
                response = self.client.post('/api/v1/payments/', self.payment_data, format='json')
                
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(response.data['status'], 'success')
                self.assertEqual(response.data['message'], 'Payment initiated successfully.')
                self.assertIn('approval_url', response.data)
                
                payment = Payment.objects.first()
                self.assertEqual(payment.customer_name, self.payment_data['customer_name'])
                self.assertEqual(payment.customer_email, self.payment_data['customer_email'])
                self.assertEqual(str(payment.amount), self.payment_data['amount'])
                self.assertEqual(payment.status, 'processing')

    def test_get_payment(self):
        payment = Payment.objects.create(**self.payment_data, status='completed')
        
        response = self.client.get(f'/api/v1/payments/{payment.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Payment details retrieved successfully.')
        self.assertEqual(response.data['payment']['customer_name'], self.payment_data['customer_name'])
        self.assertEqual(response.data['payment']['status'], 'completed')

    def test_invalid_amount(self):
        invalid_data = self.payment_data.copy()
        invalid_data['amount'] = '-50.00'
        
        response = self.client.post('/api/v1/payments/', invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payment_success_callback(self):
        payment = Payment.objects.create(**self.payment_data, status='processing')
        
        with patch('paypalrestsdk.Payment.find') as mock_find:
            mock_payment = type('Payment', (), {'execute': lambda x: True})()
            mock_find.return_value = mock_payment
            
            response = self.client.get(
                f'/api/v1/payments/{payment.id}/success/',
                {'PayerID': 'test-payer-id'}
            )
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['status'], 'success')
            self.assertEqual(response.data['message'], 'Payment completed successfully.')
            
            payment.refresh_from_db()
            self.assertEqual(payment.status, 'completed')
