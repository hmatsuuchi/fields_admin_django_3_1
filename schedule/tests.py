from datetime import date, timedelta
# django imports
from django.contrib.auth.models import User, Group
from django.test import TestCase
# drf imports
from rest_framework import status
from rest_framework.test import APIClient
# model imports
from user_profiles.models import UserProfilesInstructors
from students.models import Students, PrefectureChoices, PhoneChoice, Phone, GradeChoices, StatusChoices, PaymentChoices
from .models import Events, EventType


# ======= Events All View Tests =======
# ------- tests access permissions -------

# users NOT logged in CANNOT access the events all view
class EventsAllViewAsUnauthenticatedUserTest(TestCase):
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

# ------- tests content retrieval -------

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

# ======= Events Details View Tests =======
# ------- tests access permissions -------

# users NOT logged in CANNOT access the events details view
class EventsDetailsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_events_details_view_get(self):
        # attempt to access events details view
        response = self.client.get('/api/schedule/events/details/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the events details view
class EventsDetailsViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_events_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the events details view
class EventsDetailsViewAsCustomerGroupTest(TestCase):
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

    def test_events_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the events details view
class EventsDetailsViewAsStaffGroupTest(TestCase):
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

        # create new event type
        event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create new event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        # save event
        self.event.save()

    def test_events_details_view_get(self):
        # sets student profile id
        params = {'event_id': self.event.id}

        # attempt to access events all view
        response = self.client.get('/api/schedule/events/details/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ------- tests content retrieval -------

# properly authenticated users CAN retrieve content from the events Details view
class EventsDetailsViewContentRetrievalTest(TestCase):
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

        # create event type
        self.event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create test event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=self.event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        self.event.save()

    def test_events_details_view(self):
        # sets student profile id
        params = {'event_id': self.event.id}

        # attempt to access events all view
        response = self.client.get('/api/schedule/events/details/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response content is JSON
        self.assertEqual(response['content-type'], 'application/json')

        # response content contains event data
        self.assertEqual(response.data['id'], self.event.id)
        self.assertEqual(response.data['event_name'], 'Test Event')
        self.assertEqual(response.data['event_type']['name'], 'Test Event Type')
        self.assertEqual(response.data['event_type']['duration'], 60)
        self.assertEqual(response.data['event_type']['capacity'], 6)
        self.assertEqual(response.data['primary_instructor'], self.user.id)
        self.assertEqual(response.data['day_of_week'], 1)
        self.assertEqual(response.data['start_time'], '12:00:00')

# ======= Event Choices View Tests =======
# ------- tests access permissions -------

# users NOT logged in CANNOT access the event choices view
class EventChoicesViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_event_choices_view_get(self):
        # attempt to access events details view
        response = self.client.get('/api/schedule/events/choices/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the event choices view
class EventChoicesViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_event_choices_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the event choices view
class EventChoicesViewAsCustomerGroupTest(TestCase):
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

    def test_event_choices_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the event choices view
class EventChoicesViewAsStaffGroupTest(TestCase):
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

    def test_event_choices_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/choices/')

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ------- tests content retrieval -------

# properly authenticated users CAN retrieve content from the event choices view
class EventChoicesViewContentRetrievalTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # create test user profile
        self.user_profile = UserProfilesInstructors.objects.create(user=self.user, last_name_romaji='Test', first_name_romaji='User', last_name_katakana='テスト', first_name_katakana='ユーザー', last_name_kanji='試験', first_name_kanji='ユーザー', icon_stub='test_user_icon_stub', archived=False)

        # add test user to 'Staff' and 'Instructors' group
        staff_group = Group.objects.create(name='Staff')
        instructor_group = Group.objects.create(name='Instructors')
        self.user.groups.add(staff_group)
        self.user.groups.add(instructor_group)

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

        # create event type
        self.event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

    def test_event_choices_view(self):
        # attempt to access events all view
        response = self.client.get('/api/schedule/events/choices/')

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response content is JSON
        self.assertEqual(response['content-type'], 'application/json')

        # response content contains event choice data
        self.assertEqual(response.data['event_type_choices'][0]['id'], self.event_type.id)
        self.assertEqual(response.data['event_type_choices'][0]['name'], self.event_type.name)

        # response content contains instructor profile data
        self.assertEqual(response.data['primary_instructor_choices'][0]['userprofilesinstructors__last_name_romaji'], self.user_profile.last_name_romaji)
        self.assertEqual(response.data['primary_instructor_choices'][0]['userprofilesinstructors__first_name_romaji'], self.user_profile.first_name_romaji)
        self.assertEqual(response.data['primary_instructor_choices'][0]['userprofilesinstructors__last_name_katakana'], self.user_profile.last_name_katakana)
        self.assertEqual(response.data['primary_instructor_choices'][0]['userprofilesinstructors__first_name_katakana'], self.user_profile.first_name_katakana)
        self.assertEqual(response.data['primary_instructor_choices'][0]['userprofilesinstructors__last_name_kanji'], self.user_profile.last_name_kanji)
        self.assertEqual(response.data['primary_instructor_choices'][0]['userprofilesinstructors__first_name_kanji'], self.user_profile.first_name_kanji)

# ======= Remove Student from Event View Tests =======
# ------- tests access permissions -------

# users NOT logged in CANNOT access the remove student from event view
class RemoveStudentFromEventViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_remove_student_from_event_view_post(self):
        # attempt to access remove student from event view
        response = self.client.post('/api/schedule/events/remove_student_from_event/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the remove student from event view
class RemoveStudentFromEventViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_remove_student_from_event_view_post(self):
        # attempt to access remove student from event view
        response = self.client.post('/api/schedule/events/remove_student_from_event/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the remove student from event view
class RemoveStudentFromEventViewAsCustomerGroupTest(TestCase):
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

    def test_remove_student_from_event_view_post(self):
        # attempt to access remove student from event view
        response = self.client.post('/api/schedule/events/remove_student_from_event/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the remove student from event view
class RemoveStudentFromEventViewAsStaffGroupTest(TestCase):
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

        # create test prefecture choice
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

        # create new event type
        event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create new event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        # save event
        self.event.save()

        # add test profile to event
        self.event.students.add(self.test_profile)

    def test_remove_student_from_event_view_put(self):
        # set data payload
        params = {'event_id': self.event.id, 'student_id': self.test_profile.id}

        # attempt to access remove student from event view
        response = self.client.put('/api/schedule/events/remove_student_from_event/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ------- tests student removal action -------
class RemoveStudentFromEventViewActionTest(TestCase):
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

        # create test prefecture choice
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

        # create new event type
        event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create new event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        # save event
        self.event.save()

        # add test profile to event
        self.event.students.add(self.test_profile)

        # confirm test profile is in event
        self.assertEqual(self.event.students.count(), 1)

    def test_remove_student_from_event_view_put(self):
        # set data payload
        params = {'event_id': self.event.id, 'student_id': self.test_profile.id}

        # attempt to access remove student from event view
        response = self.client.put('/api/schedule/events/remove_student_from_event/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # confirm test profile is NOT in event
        self.assertEqual(self.event.students.count(), 0)

# ======= Add Student to Event View Tests =======
# ------- tests access permissions -------

# users NOT logged in CANNOT access the add student to event view
class AddStudentToEventViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_add_student_to_event_view_post(self):
        # attempt to access add student to event view
        response = self.client.post('/api/schedule/events/add_student_to_event/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the add student to event view
class AddStudentToEventViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_add_student_to_event_view_post(self):
        # attempt to access add student to event view
        response = self.client.post('/api/schedule/events/add_student_to_event/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the add student to event view
class AddStudentToEventViewAsCustomerGroupTest(TestCase):
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

    def test_add_student_to_event_view_post(self):
        # attempt to access add student to event view
        response = self.client.post('/api/schedule/events/add_student_to_event/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the add student to event view
class AddStudentToEventViewAsStaffGroupTest(TestCase):
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

        # create test prefecture choice
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

        # create new event type
        event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create new event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        # save event
        self.event.save()

        # add test profile to event
        self.event.students.add(self.test_profile)

    def test_add_student_to_event_view_put(self):
        # set data payload
        params = {'event_id': self.event.id, 'student_id': self.test_profile.id}

        # attempt to access remove student from event view
        response = self.client.put('/api/schedule/events/add_student_to_event/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ------- tests student add action -------
class AddStudentToEventViewActionTest(TestCase):
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

        # create test prefecture choice
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

        # create new event type
        event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create new event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        # save event
        self.event.save()

        # confirm test profile is NOT in event
        self.assertEqual(self.event.students.count(), 0)

    def test_add_student_to_event_view_put(self):
        # set data payload
        params = {'event_id': self.event.id, 'student_id': self.test_profile.id}

        # attempt to access remove student from event view
        response = self.client.put('/api/schedule/events/add_student_to_event/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # confirm test profile is NOT in event
        self.assertEqual(self.event.students.count(), 1)

# ======= Archive Event View Tests =======
# ------- tests access permissions -------

# users NOT logged in CANNOT access the archive event view
class ArchiveEventViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_archive_event_view_post(self):
        # attempt to access archive event view
        response = self.client.post('/api/schedule/events/archive_event/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the archive event view
class ArchiveEventViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # set test user as authenticated
        self.client.force_authenticate(user=self.user)

    def test_archive_event_view_post(self):
        # attempt to access archive event view
        response = self.client.post('/api/schedule/events/archive_event/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the archive event view
class ArchiveEventViewAsCustomerGroupTest(TestCase):
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

    def test_archive_event_view_post(self):
        # attempt to access archive event view
        response = self.client.post('/api/schedule/events/archive_event/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the archive event view
class ArchiveEventViewAsStaffGroupTest(TestCase):
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

        # create new event type
        event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create new event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        # save event
        self.event.save()

    def test_archive_event_view_put(self):
        # set data payload
        params = {'event_id': self.event.id}

        # attempt to access archive event view
        response = self.client.put('/api/schedule/events/archive_event/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ------- tests event archive action -------

class ArchiveEventViewActionTest(TestCase):
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

        # create new event type
        event_type = EventType.objects.create(name='Test Event Type', price=999, duration=60, order=1, capacity=6)

        # create new event
        self.event = Events.objects.create(
            event_name='Test Event',
            event_type=event_type,
            primary_instructor=self.user,
            day_of_week=1,
            start_time='12:00:00',
        )

        # save event
        self.event.save()

    def test_archive_event_view_put(self):
        # get event from database
        event_from_db = Events.objects.get(id=self.event.id)

        # test event is NOT archived
        self.assertFalse(event_from_db.archived)

        # set data payload
        params = {'event_id': self.event.id}

        # attempt to access archive event view
        response = self.client.put('/api/schedule/events/archive_event/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get event from database
        event_from_db = Events.objects.get(id=self.event.id)

        # test event is archived
        self.assertTrue(event_from_db.archived)