from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# GROUP PERMISSION CONTROL
from authentication.permissions import isInStaffGroup
# AUTHENTICATION
from authentication.customAuthentication import CustomAuthentication
# MODELS
from .models import Invoice, InvoiceItem, PaymentMethod, ServiceType, Tax
from django.db.models import Prefetch
from students.models import Students
# SERIALIZERS
from .serializers import InvoiceListAllSerializer, InvoiceStatusAllSerializer, InvoiceCreateSerializer, ProfilesListForSelectSerializer, PaymentMethodSerializer, ServiceTypeSerializer, TaxSerializer

# Invoice List All View
class InvoiceListAllView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - event type choice list
    def get(self, request, format=None):
        try:

            # get all invoices, prefetch invoice items and eager-load InvoiceItem FKs
            invoice_items_qs = InvoiceItem.objects.select_related('invoice', 'service_type', 'tax_type', 'service_type__tax')
            invoices_all = (
                Invoice.objects
                .select_related('student', 'payment_method')
                .prefetch_related(Prefetch('invoiceitem_set', queryset=invoice_items_qs))
                .order_by('-id')
            )

            # serialize data
            serializer = InvoiceListAllSerializer(invoices_all, many=True)
            
            data = {
                'invoices': serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# Invoice Status All View
class InvoiceStatusAllView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET - event type choice list
    def get(self, request, format=None):
        try:
            # get year and month values from query params
            year = request.query_params.get('year', None)
            month = request.query_params.get('month', None)
            display_unissued_only = request.query_params.get('display_unissued_only', None)
            display_unpaid_only = request.query_params.get('display_unpaid_only', None)

            # get all invoices, prefetch invoice items and eager-load InvoiceItem FKs
            invoice_items_qs = InvoiceItem.objects.select_related('invoice', 'service_type', 'tax_type', 'service_type__tax')
            invoices_all = (
                Invoice.objects
                .select_related('student')
                .prefetch_related(Prefetch('invoiceitem_set', queryset=invoice_items_qs))
                .order_by('-id')
            )

            # apply additional filters
            if year:
                invoices_all = invoices_all.filter(year=year)
            if month:
                invoices_all = invoices_all.filter(month=month)
            if display_unissued_only == 'true':
                invoices_all = invoices_all.filter(issued_date__isnull=True)
            if display_unpaid_only == 'true':
                invoices_all = invoices_all.filter(paid_date__isnull=True)

            # serialize data
            serializer = InvoiceStatusAllSerializer(invoices_all, many=True)
            
            data = {
                'invoices': serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# Invoice Status Batch Update View
class InvoiceStatusBatchUpdateView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def post(self, request, format=None):
        try:
            updated_records = request.data

            for record in updated_records:
                record_id = record['id']
                record_field = record['field']
                record_new_value = record['newValue']

                # converts empty strings to None
                if record_new_value == "":
                    record_new_value = None

                # process each record
                invoice = Invoice.objects.get(id=record_id)
                setattr(invoice, record_field, record_new_value)
                invoice.save()

            return Response({'message': 'Invoice statuses updated successfully.'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Invoice Create View
class InvoiceCreateView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def post(self, request, format=None):
        data_copy = request.data.copy()

        # if frontend sends empty strings, convert to null
        null_if_empty_fields = ['transfer_date', 'paid_date']

        for field in null_if_empty_fields:
            if data_copy.get(field) == "":
                data_copy[field] = None

        try:
            serializer = InvoiceCreateSerializer(data=data_copy)

            if serializer.is_valid():
                invoice = serializer.save()
            
                return Response({'invoice_id': invoice.id}, status=status.HTTP_200_OK)
            
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        
# Payment method for select list
class PaymentMethodsListForSelectView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def get(self, request, format=None):
        try:
            payment_methods = PaymentMethod.objects.all().order_by('order')

            serializer = PaymentMethodSerializer(payment_methods, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

            
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
# Service Types for select list
class ServiceTypesListForSelectView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def get(self, request, format=None):
        try:
            service_types = ServiceType.objects.all().order_by('order').select_related('tax')

            serializer = ServiceTypeSerializer(service_types, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

            
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
# Taxes for select list
class TaxesListForSelectView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def get(self, request, format=None):
        try:
            taxes = Tax.objects.all().order_by('order')
            taxes_serializer = TaxSerializer(taxes, many=True)

            default_tax = taxes.filter(default_value=True).first()
            default_tax_id = default_tax.id if default_tax else ""

            return Response({'taxes': taxes_serializer.data, 'default_tax': default_tax_id}, status=status.HTTP_200_OK)

            
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)