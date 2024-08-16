from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Events, EventType

# ======= Events All View Tests (tests access permissions) =======

# users NOT logged in CANNOT access the events all view
class EventsAllViewAsUnauthenticatedUserTests(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_events_all_view(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/')

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
        response = self.client.get('/api/schedule/events/')

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
        response = self.client.get('/api/schedule/events/')

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
        response = self.client.get('/api/schedule/events/')

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ======= Events All View Tests (tests content retrieval) =======

# properly authenticated users CAN retrieve content from the events all view
class EventsAllViewContentRetrievalTest(TestCase):
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

        # create event types
        event_type_1 = EventType.objects.create(name='Test Event Type 1', price=999, duration=60, order=1, capacity=6)
        event_type_2 = EventType.objects.create(name='Test Event Type 2', price=999, duration=60, order=2, capacity=6)
        event_type_3 = EventType.objects.create(name='Test Event Type 3', price=999, duration=60, order=3, capacity=6)

        # create test events
        event_1 = Events.objects.create(
            event_name='Test Event 1',
            event_type=event_type_1,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )
        event_2 = Events.objects.create(
            event_name='Test Event 2',
            event_type=event_type_2,
            primary_instructor=self.user,
            day_of_week=2,
            start_time='12:00:00',
        )
        event_3 = Events.objects.create(
            event_name='Test Event 3',
            event_type=event_type_3,
            primary_instructor=self.user,
            day_of_week=3,
            start_time='12:00:00',
        )
        event_1.save()
        event_2.save()
        event_3.save()

    def test_events_all_view(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/')

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response content is JSON
        self.assertEqual(response['content-type'], 'application/json')

        # response content contains event data
        self.assertEqual(len(response.data['events']), 3) # should fetch all three previously created events

# ======= Events Details View Tests (test access permissions) =======

# users NOT logged in CANNOT access the events details view
class EventsDetailsViewAsUnauthenticatedUserTests(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_events_details_view(self):
        # attempt to access events details view
        response = self.client.get('/api/schedule/events/details/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)