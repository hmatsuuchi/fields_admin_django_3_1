from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class ProfilesListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # create staff group
        self.group = Group.objects.create(name='Staff')
        # add user to staff group
        self.user.groups.add(self.group)

        # generate simple JWT token for user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)


    def test_profiles_list_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)