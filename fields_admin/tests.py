from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APIClient

# Unauthenticated users CANNOT access the logged in user data view
class LoggedInUserDataViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/logged_in_user_data/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Authenticated users with no group CAN access the logged in user data view
class LoggedInUserDataViewAsAuthenticatedUserNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/logged_in_user_data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logged_in_user_data', response.data)
        self.assertIn('logged_in_user_groups', response.data)

# Authenticated users in Staff group CAN access the logged in user data view
class LoggedInUserDataViewAsAuthenticatedUserInStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/logged_in_user_data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logged_in_user_data', response.data)
        self.assertIn('logged_in_user_groups', response.data)
        self.assertIn('Staff', response.data['logged_in_user_groups'])

# Authenticated users in Customers group CAN access the logged in user data view
class LoggedInUserDataViewAsAuthenticatedUserInCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/logged_in_user_data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logged_in_user_data', response.data)
        self.assertIn('logged_in_user_groups', response.data)
        self.assertIn('Customers', response.data['logged_in_user_groups'])

# Authenticated users in multiple groups CAN access the logged in user data view
class LoggedInUserDataViewAsAuthenticatedUserInMultipleGroupsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(staff_group, instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/logged_in_user_data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('logged_in_user_data', response.data)
        self.assertIn('logged_in_user_groups', response.data)
        self.assertIn('Staff', response.data['logged_in_user_groups'])
        self.assertIn('Instructors', response.data['logged_in_user_groups'])

# Test that the response contains correct user data
class LoggedInUserDataViewResponseDataTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='johndoe', 
            password='testpassword',
        )
        self.client.force_authenticate(user=self.user)

    def test_response_contains_user_info(self):
        response = self.client.get('/api/logged_in_user_data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = response.data['logged_in_user_data']
        self.assertEqual(user_data['username'], 'johndoe')

# Test that the response contains correct group information
class LoggedInUserDataViewResponseGroupsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(administrators_group, displays_group)
        self.client.force_authenticate(user=self.user)

    def test_response_groups_list(self):
        response = self.client.get('/api/logged_in_user_data/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        groups = response.data['logged_in_user_groups']
        self.assertEqual(len(groups), 2)
        self.assertIn('Administrators', groups)
        self.assertIn('Displays', groups)