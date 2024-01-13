from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

import json

# users NOT in any group CANNOT access the student profiles list view
class ProfilesListViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_profiles_list_view(self):
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users in the 'Customers' group CANNOT access the student profiles list view
class ProfilesListViewAsCustomerGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Customers')
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_profiles_list_view(self):
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users in the 'Staff' group CAN access the student profiles list view
class ProfilesListViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Staff')
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_profiles_list_view(self):
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# users in the 'Staff' group CAN access the student details view
class ProfilesDetailsViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Staff')
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': '',
            'first_name_romaji': '',
            'last_name_kanji': '',
            'first_name_kanji': '',
            'last_name_katakana': '',
            'first_name_katakana': '',
            'post_code': '',
            'prefecture': '',
            'city': '',
            'address_1': '',
            'address_2': '',
            'phone': [],
            'birthday': '',
            'grade': '',
            'status': '',
            'payment_method': '',
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)