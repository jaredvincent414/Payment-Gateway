from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from .services import PaymentGatewayService

# Create your views here.

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        # Initialize payment with PayPal
        result = PaymentGatewayService.create_paypal_payment(payment)
        if result:
            return Response({
                "payment": serializer.data,
                "approval_url": result["approval_url"],
                "status": "success",
                "message": "Payment initiated successfully."
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "message": "Failed to initiate payment."
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "payment": serializer.data,
            "status": "success",
            "message": "Payment details retrieved successfully."
        })

    @action(detail=True, methods=['get'])
    def success(self, request, *args, **kwargs):
        payment = self.get_object()
        payer_id = request.query_params.get('PayerID')
        
        if not payer_id:
            return Response({
                "status": "error",
                "message": "PayerID is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        if PaymentGatewayService.execute_paypal_payment(payment, payer_id):
            serializer = self.get_serializer(payment)
            return Response({
                "payment": serializer.data,
                "status": "success",
                "message": "Payment completed successfully."
            })
        
        return Response({
            "status": "error",
            "message": "Payment execution failed."
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def cancel(self, request, *args, **kwargs):
        payment = self.get_object()
        payment.status = 'failed'
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response({
            "payment": serializer.data,
            "status": "cancelled",
            "message": "Payment was cancelled."
        })
