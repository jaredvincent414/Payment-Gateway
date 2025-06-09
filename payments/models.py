from django.db import models
import uuid

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_gateway = models.CharField(max_length=20, default='paypal')  # paypal, paystack, or flutterwave
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gateway_reference = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} - {self.customer_name} - {self.amount}"

    class Meta:
        ordering = ['-created_at']
