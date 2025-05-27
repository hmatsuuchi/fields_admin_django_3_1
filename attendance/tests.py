from django.test import TestCase
# django imports
from django.contrib.auth.models import User, Group
from django.urls import reverse
# drf imports
from rest_framework import status
from rest_framework.test import APIClient
# json imports
import json
# model imports
from .models import Attendance, AttendanceRecord, AttendanceRecordStatus
from schedule.models import Events, EventType
from students.models import Students, GradeChoices, StatusChoices
from user_profiles.models import UserProfilesInstructors

# ======= ATTENDANCE FOR DATE VIEW TESTS - ACCESS PERMISSIONS =======

# users NOT logged in CANNOT access the attendance for date view
class AttendanceForDateViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the attendance for date view
class AttendanceForDateViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' groupd CANNOT access the attendance for date view
class AttendanceForDateViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Customers' group
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the attendance for date view
class AttendanceForDateViewAsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Staff' group
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_for_date_view_get(self):
        params = {
            'date': '2022-01-01',
            'instructor_id': self.user.id,
        }

        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ======= ATTENDANCE FOR DATE VIEW TESTS - DATA RETRIEVAL =======

# properly authenticated users CAN retrieve data from the attendance for date view
class AttendanceForDateViewAContentRetrievalTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Staff' group
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

        # create student
        self.student = Students()
        self.student.last_name_romaji = 'Test Student Last'
        self.student.first_name_romaji = 'Test Student First'
        self.student.save()

        # create event type
        self.event_type = EventType()
        self.event_type.name = 'Test Event Type'
        self.event_type.price = 9999
        self.event_type.duration = 99
        self.event_type.order = 99
        self.event_type.capacity = 9
        self.event_type.save()

        # create events
        self.event = Events()
        self.event.event_name = 'Test Event'
        self.event.event_type = self.event_type
        self.event.primary_instructor = self.user
        self.event.day_of_week = 1
        self.event.start_time = '01:01:01'
        self.event.archived = False
        self.event.save()

        self.event.students.add(self.student)

        # create attendance records status
        self.attendance_record_status = AttendanceRecordStatus()
        self.attendance_record_status.status_name = 'Test Status'
        self.attendance_record_status.save()

        # create grade choices
        self.grade_choice = GradeChoices()
        self.grade_choice.name = 'Test Grade'
        self.grade_choice.order = 99
        self.grade_choice.save()

        # create attendance records
        self.attendance_record = AttendanceRecord()
        self.attendance_record.student = self.student
        self.attendance_record.status = self.attendance_record_status
        self.attendance_record.grade = self.grade_choice
        self.attendance_record.save()

        # create attendances
        self.attendance = Attendance()
        self.attendance.linked_class = self.event
        self.attendance.instructor = self.user
        self.attendance.date = '2022-01-01'
        self.attendance.start_time = '01:01:01'
        self.attendance.save()

        self.attendance.attendance_records.add(self.attendance_record)

    def test_attendance_for_date_view_get(self):
        params = {
            'date': '2022-01-01',
            'instructor_id': self.user.id,
        }

        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/', params)

        # response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response conent is JSON
        self.assertEqual(response['content-type'], 'application/json')

        # gets response data
        response_data = response.data['attendance'][0]
        
        # checks response data
        self.assertEqual(response_data['date'], '2022-01-01')
        self.assertEqual(response_data['start_time'], '01:01:01')

        self.assertEqual(response_data['linked_class']['event_name'], 'Test Event')

        self.assertEqual(response_data['linked_class']['event_type']['duration'], 99)
        self.assertEqual(response_data['linked_class']['event_type']['capacity'], 9)

        self.assertEqual(response_data['instructor']['username'], 'testuser')

        self.assertEqual(response_data['attendance_records'][0]['student']['last_name_romaji'], 'Test Student Last')
        self.assertEqual(response_data['attendance_records'][0]['student']['first_name_romaji'], 'Test Student First')

# ======= ATTENDANCE DETAILS VIEW TESTS - ACCESS PERMISSIONS =======

# users NOT logged in CANNOT access the attendance details view
class AttendanceDetailsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_attendance_details_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the attendance details view
class AttendanceDetailsViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_details_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users looged in but in the 'Customers' group CANNOT access the attendance details view
class AttendanceDetailsViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Customers' group
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_details_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the attendance details view
class AttendanceDetailsViewAsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Staff' group
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

        # create event type
        self.event_type = EventType()
        self.event_type.duration = 99
        self.event_type.capacity = 9
        self.event_type.save()

        # create linked class
        self.linked_class = Events()
        self.linked_class.event_name = 'Test Event'
        self.linked_class.event_type = self.event_type
        self.linked_class.primary_instructor = self.user
        self.linked_class.day_of_week = 1
        self.linked_class.start_time = '01:01:01'
        self.linked_class.save()

        # create grade choice
        self.grade_choice = GradeChoices()
        self.grade_choice.name = 'Test Grade'
        self.grade_choice.order = 99
        self.grade_choice.save()

        # create status choice
        self.status_choice = StatusChoices()
        self.status_choice.name = 'Test Status'
        self.status_choice.order = 99
        self.status_choice.save()

        # create attendance record status
        self.attendance_record_status = AttendanceRecordStatus()
        self.attendance_record_status.status_name = 'Test Status'
        self.attendance_record_status.save()

        # create student
        self.student = Students()
        self.student.last_name_romaji = 'Test Student Last'
        self.student.first_name_romaji = 'Test Student First'
        self.student.last_name_kanji = '試験'
        self.student.first_name_kanji = '学生'
        self.student.last_name_katakana = 'テスト'
        self.student.first_name_katakana = 'ガクセイ'
        self.student.grade = self.grade_choice
        self.student.status = self.status_choice
        self.student.save()

        # create attendance record
        self.attendance_record = AttendanceRecord()
        self.attendance_record.student = self.student
        self.attendance_record.status = self.attendance_record_status
        self.attendance_record.grade = self.grade_choice
        self.attendance_record.save()

        # create user profile instructor
        self.user_profile_instructor = UserProfilesInstructors()
        self.user_profile_instructor.user = self.user
        self.user_profile_instructor.last_name_romaji = 'Test Instructor Last'
        self.user_profile_instructor.first_name_romaji = 'Test Instructor First'
        self.user_profile_instructor.icon_stub = '/media/test_instructor_icon.jpg'
        self.user_profile_instructor.save()

        # create attendance
        self.attendance = Attendance()
        self.attendance.linked_class = self.linked_class
        self.attendance.instructor = self.user
        self.attendance.date = '2022-01-01'
        self.attendance.start_time = '01:01:01'
        self.attendance.save()

    def test_attendance_details_view_post(self):
        json_data = {
            'linked_class': self.linked_class.id,
            'instructor': self.user.id,
            'date': '2022-01-01',
            'start_time': '01:01:01',
            'attendance_records':
            [{
                    'student': self.student.id,
                    'status': self.attendance_record_status.id,
                    'grade': self.grade_choice.id,
                },
            ],
        }

        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/', json.dumps(json_data), content_type='application/json')

        # response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# ======= ATTENDANCE DETAILS VIEW TESTS - DATA CREATION/UPDATE/DELETION =======

# properly authenticated users CAN create/update/delete data from the attendance details view
class AttendanceDetailsViewContentRetrievalTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Staff' group
        self.staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(self.staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

        # create grade
        self.grade = GradeChoices.objects.create(name='Test Grade', order=99)

        # create student
        self.student = Students()
        self.student.last_name_romaji = 'Test Student Last'
        self.student.first_name_romaji = 'Test Student First'
        self.student.grade = self.grade
        self.student.save()

        # create event type
        self.event_type = EventType()
        self.event_type.name = 'Test Event Type'
        self.event_type.price = 9999
        self.event_type.duration = 99
        self.event_type.order = 99
        self.event_type.capacity = 9
        self.event_type.save()

        # create events
        self.event = Events()
        self.event.event_name = 'Test Event'
        self.event.event_type = self.event_type
        self.event.primary_instructor = self.user
        self.event.day_of_week = 1
        self.event.start_time = '01:01:01'
        self.event.archived = False
        self.event.save()

        self.event.students.add(self.student)

        # create attendance records status
        self.attendance_record_status = AttendanceRecordStatus()
        self.attendance_record_status.status_name = 'Test Status'
        self.attendance_record_status.save()

        # create grade choices
        self.grade_choice = GradeChoices()
        self.grade_choice.name = 'Test Grade'
        self.grade_choice.order = 99
        self.grade_choice.save()

        # create attendance records
        self.attendance_record = AttendanceRecord()
        self.attendance_record.student = self.student
        self.attendance_record.status = self.attendance_record_status
        self.attendance_record.grade = self.grade_choice
        self.attendance_record.save()

        # create attendances
        self.attendance = Attendance()
        self.attendance.linked_class = self.event
        self.attendance.instructor = self.user
        self.attendance.date = '2022-01-01'
        self.attendance.start_time = '01:01:01'
        self.attendance.save()

        self.attendance.attendance_records.add(self.attendance_record)

    # test creation of attendance and attendance record
    def test_attendance_details_view_post(self):
        url = reverse('attendance_details')

        payload = {
            "linked_class": self.event.id,
            "instructor": self.event.primary_instructor.id,
            "date": "2025-05-15",
            "start_time": "09:00:00",
            "attendance_records": [
                {
                    "student": self.student.id,
                    "status": self.attendance_record_status.id,
                    "grade": self.grade.id
                }
            ]
        }

        response = self.client.post(url, payload, format='json')

        # check to make sure record was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check to make sure response data is correct
        response_data = response.data

        self.assertEqual(response_data['date'], '2025-05-15')
        self.assertEqual(response_data['start_time'], '09:00:00')
        self.assertEqual(response_data['linked_class'], self.event.id)
        self.assertEqual(response_data['instructor'], self.user.id)

        self.assertEqual(len(response_data['attendance_records']), 1)
        self.assertEqual(response_data['attendance_records'][0]['student'], self.student.id)
        self.assertEqual(response_data['attendance_records'][0]['status'], self.attendance_record_status.id)
        self.assertEqual(response_data['attendance_records'][0]['grade'], self.grade.id)

    # test updating an existing attendance and attendance record
    def test_attendance_details_view_put(self):
        url = reverse('attendance_details')

        payload = {
            "attendance_id": self.attendance.id,
            "start_time": "12:12:12",
        }

        response = self.client.put(url, payload, format='json')

        # check to make sure record was updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check to make sure time was updated and other data is intact
        response_data = response.data

        self.assertEqual(response_data['date'], '2022-01-01')
        self.assertEqual(response_data['start_time'], '12:12:12')
        self.assertEqual(response_data['linked_class'], self.event.id)
        self.assertEqual(response_data['instructor'], self.user.id)

        self.assertEqual(len(response_data['attendance_records']), 1)
        self.assertEqual(response_data['attendance_records'][0]['student'], self.student.id)
        self.assertEqual(response_data['attendance_records'][0]['status'], self.attendance_record_status.id)
        self.assertEqual(response_data['attendance_records'][0]['grade'], self.attendance_record.grade.id)

    # test deleting an existing attendance and attendance record
    def test_attendance_details_view_delete(self):
        # check to make sure attendance exists before deletion
        self.assertTrue(Attendance.objects.filter(id=self.attendance.id).exists())

        url = reverse('attendance_details')

        payload = {
            "attendance_id": self.attendance.id,
        }

        response = self.client.delete(url, payload, format='json')

        # check to make sure record was deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check to make sure attendance no longer exists
        with self.assertRaises(Attendance.DoesNotExist):
            Attendance.objects.get(id=self.attendance.id)