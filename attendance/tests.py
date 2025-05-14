from django.test import TestCase
# django imports
from django.contrib.auth.models import User, Group
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

# ======= Attendance For Date View Tests =======

# ------- tests access permissions -------

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

# ------- tests data retrieval -------

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
        student = Students()
        student.last_name_romaji = 'Test Student Last'
        student.first_name_romaji = 'Test Student First'
        student.save()

        # create event type
        event_type = EventType()
        event_type.name = 'Test Event Type'
        event_type.price = 9999
        event_type.duration = 99
        event_type.order = 99
        event_type.capacity = 9
        event_type.save()

        # create events
        event = Events()
        event.event_name = 'Test Event'
        event.event_type = event_type
        event.primary_instructor = self.user
        event.day_of_week = 1
        event.start_time = '01:01:01'
        event.archived = False
        event.save()

        event.students.add(student)

        # create attendance records status
        attendance_record_status = AttendanceRecordStatus()
        attendance_record_status.status_name = 'Test Status'
        attendance_record_status.save()

        # create grade choices
        grade_choice = GradeChoices()
        grade_choice.name = 'Test Grade'
        grade_choice.order = 99
        grade_choice.save()

        # create attendance records
        attendance_record = AttendanceRecord()
        attendance_record.student = student
        attendance_record.status = attendance_record_status
        attendance_record.grade = grade_choice
        attendance_record.save()

        # create attendances
        attendance = Attendance()
        attendance.linked_class = event
        attendance.instructor = self.user
        attendance.date = '2022-01-01'
        attendance.start_time = '01:01:01'
        attendance.save()

        attendance.attendance_records.add(attendance_record)

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

# ======= Attendance Details View Tests =======

# ------- tests access permissions -------

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
                    'status': self.status_choice.id,
                    'grade': self.grade_choice.id,
                },
            ],
        }

        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/', json.dumps(json_data), content_type='application/json')

        # response status code is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# ------- tests data retrieval -------
# properly authenticated users CAN retrieve data from the attendance details view