from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# GROUP PERMISSION CONTROL
from authentication.permissions import isInStaffGroup
# AUTHENTICATION
from authentication.customAuthentication import CustomAuthentication
# MODELS
from .models import Invoice, InvoiceItem
from django.db.models import Prefetch
from students.models import Students
# SERIALIZERS
from .serializers import InvoiceSerializer
from .serializers import ProfilesListForSelectSerializer

# Invoice List All View
class InvoiceListAllView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - event type choice list
    def get(self, request, format=None):
        try:

            # get all invoices, prefetch invoice items and eager-load InvoiceItem FKs
            invoice_items_qs = InvoiceItem.objects.select_related('service_type', 'service_type__tax')
            invoices_all = (
                Invoice.objects
                .select_related('student', 'payment_method')
                .prefetch_related(Prefetch('invoiceitem_set', queryset=invoice_items_qs))
            )

            # serialize data
            serializer = InvoiceSerializer(invoices_all, many=True)
            
            data = {
                'invoices': serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# Profiles for customer select list
class ProfilesListForSelectView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def get(self, request, format=None):
        try:
            profiles = Students.objects.all().order_by('-id').select_related('prefecture', 'grade')

            serializer = ProfilesListForSelectSerializer(profiles, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

            
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)