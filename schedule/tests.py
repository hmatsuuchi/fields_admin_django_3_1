from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# ======= Events All View Tests (tests access permissions) =======

# users NOT logged in CANNOT access the events all view
class EventsAllViewAsUnauthenticatedUserTests(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_events_all_view(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/all/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the events all view
class EventsAllViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_events_all_view(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/all/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the events all view
class EventsAllViewAsCustomerGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # add test user to 'Customers' group
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_events_all_view(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/all/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the events all view
class EventsAllViewAsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # add test user to 'Staff' group
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_events_all_view(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/all/')

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)