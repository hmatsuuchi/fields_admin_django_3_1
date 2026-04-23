from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.permissions import isInStaffGroup
from authentication.customAuthentication import CustomAuthentication
from .serializers import JournalEntryCreateSerializer, JournalEntrySerializer


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
