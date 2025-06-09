import paypalrestsdk
from django.conf import settings
from .models import Payment

class PaymentGatewayService:
    @staticmethod
    def initialize_paypal():
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,  # sandbox or live
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

    @staticmethod
    def create_paypal_payment(payment: Payment):
        PaymentGatewayService.initialize_paypal()
        
        paypal_payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(payment.amount),
                    "currency": "USD"
                },
                "description": f"Payment for {payment.customer_name}"
            }],
            "redirect_urls": {
                "return_url": f"{settings.BASE_URL}/api/v1/payments/{payment.id}/success",
                "cancel_url": f"{settings.BASE_URL}/api/v1/payments/{payment.id}/cancel"
            }
        })

        if paypal_payment.create():
            payment.gateway_reference = paypal_payment.id
            payment.status = 'processing'
            payment.save()
            
            # Get the approval URL
            for link in paypal_payment.links:
                if link.rel == "approval_url":
                    return {"approval_url": link.href}
        
        payment.status = 'failed'
        payment.save()
        return None

    @staticmethod
    def execute_paypal_payment(payment: Payment, payer_id: str):
        PaymentGatewayService.initialize_paypal()
        
        paypal_payment = paypalrestsdk.Payment.find(payment.gateway_reference)
        if paypal_payment.execute({"payer_id": payer_id}):
            payment.status = 'completed'
            payment.save()
            return True
        
        payment.status = 'failed'
        payment.save()
        return False 