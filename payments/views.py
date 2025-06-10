# payments/views.py
from rest_framework.views import APIView # Importing APIView for creating API endpoints
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer

class InitiatePayment(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({
                "payment_id": payment.id,
                "status": "success",
                "message": "Payment initiated successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrievePayment(APIView):
    def get(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment)
            return Response({
                "payment": serializer.data,
                "status": "success",
                "message": "Payment details retrieved successfully."
            }, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Payment not found."
            }, status=status.HTTP_404_NOT_FOUND)
