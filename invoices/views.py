from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# GROUP PERMISSION CONTROL
from authentication.permissions import isInStaffGroup
# AUTHENTICATION
from authentication.customAuthentication import CustomAuthentication
# MODELS
from .models import Invoice
# SERIALIZERS
from .serializers import InvoiceSerializer

class InvoiceListAllView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - event type choice list
    def get(self, request, format=None):
        try:

            # get all invoices
            invoices_all = Invoice.objects.all().select_related('student', 'payment_method')

            # serialize data
            serializer = InvoiceSerializer(invoices_all, many=True)
            
            data = {
                'invoices': serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)