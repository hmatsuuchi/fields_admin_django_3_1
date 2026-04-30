from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.permissions import isInStaffGroup
from authentication.customAuthentication import CustomAuthentication
# SERIALIZERS
from .serializers import JournalEntryCreateSerializer, JournalEntrySerializer
# MODELS
from .models import Account
from django.db.models import Sum, Case, When, IntegerField


# creates a journal entry with line items
class JournalEntriesCreateView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def post(self, request, format=None):
        try:
            serializer = JournalEntryCreateSerializer(data=request.data)

            if serializer.is_valid():
                entry = serializer.save()
                return Response(JournalEntrySerializer(entry).data, status=status.HTTP_201_CREATED)

            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# provides a list of active accounts for dropdown menus
class AccountListForDropdownMenuView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        accounts = Account.objects.filter(archived=False).order_by('code')

        data = [{'id': acc.id, 'code': acc.code, 'name_japanese': acc.name_japanese, 'name_english': acc.name_english, 'account_type': acc.account_type} for acc in accounts]
        
        return Response(data)
    
# balance sheet
class BalanceSheetView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        accounts = Account.objects.filter(archived=False).annotate(
            total_debits=Sum(Case(
                When(journalentryline__side='DEBIT', then='journalentryline__amount'),
                default=0,
                output_field=IntegerField(),
            )),
            total_credits=Sum(Case(
                When(journalentryline__side='CREDIT', then='journalentryline__amount'),
                default=0,
                output_field=IntegerField(),
            )),
        ).order_by('code')

        data = []
        for acc in accounts:
            debits = acc.total_debits or 0
            credits = acc.total_credits or 0
            balance = (debits - credits) if acc.normal_balance == 'debit' else (credits - debits)
            data.append({
                'id': acc.id,
                'code': acc.code,
                'name_japanese': acc.name_japanese,
                'name_english': acc.name_english,
                'account_type': acc.account_type,
                'balance': balance,
            })

        return Response(data)
    
# account activity (transactions)
class AccountActivityView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        # get parameter for account_id
        account_id = request.query_params.get('account_id')

        if not account_id:
            return Response({'error': 'Account ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(id=account_id, archived=False)
        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)

        lines = account.journalentryline_set.select_related('entry').order_by('entry__date', 'entry__date_time_created')

        data = {}

        running_balance = 0
        transactions = []
        for line in lines:
            entry = line.entry
            if account.normal_balance == 'debit':
                running_balance += line.amount if line.side == 'DEBIT' else -line.amount
            else:
                running_balance += line.amount if line.side == 'CREDIT' else -line.amount

            transactions.append({
                'id': entry.id,
                'date': entry.date,
                'description': entry.description,
                'reference': entry.reference,
                'side': line.side,
                'amount': line.amount,
                'running_balance': running_balance,
            })

        transactions.reverse()  # return newest-first

        data['transactions'] = transactions
        data['account_data'] = {'account_type': account.account_type, 'account_code': account.code, 'account_name_japanese': account.name_japanese}
        
        return Response(data)