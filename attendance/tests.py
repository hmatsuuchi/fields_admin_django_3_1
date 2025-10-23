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

# ==============================================
# ======= ATTENDANCE FOR DATE VIEW TESTS =======
# ==============================================

# ============= ACCESS PERMISSIONS =============

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

# users logged in but in the 'Administrators' group CANNOT access the attendance for date view
class AttendanceForDateViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the attendance for date view
class AttendanceForDateViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the attendance for date view
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

# users logged in but in the 'Instructors' group CANNOT access the attendance for date view
class AttendanceForDateViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the attendance for date view
class AttendanceForDateViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/single_date/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the attendance for date view
class AttendanceForDateViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

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

# =============== DATA RETRIEVAL ===============

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

# ===============================================
# ======== ATTENDANCE DETAILS VIEW TESTS ========
# ===============================================

# ============= ACCESS PERMISSIONS =============

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

# users logged in but in the 'Administrators' group CANNOT access the attendance details view
class AttendanceDetailsViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_details_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the attendance details view
class AttendanceDetailsViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_details_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the attendance details view
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

# users logged in but in the 'Instructors' group CANNOT access the attendance details view
class AttendanceDetailsViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_details_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the attendance details view
class AttendanceDetailsViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_details_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/attendance_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the attendance details view
class AttendanceDetailsViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

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

# ======== DATA CREATION/UPDATE/DELETION ========

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

# ======================================================
# ======== ATTENDANCE RECORD DETAILS VIEW TESTS ========
# ======================================================

# ================= ACCESS PERMISSIONS =================

# users NOT logged in CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsCustomersGroupTest(TestCase):
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

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the attendance record details view
class AttendanceRecordDetailsViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/attendance_record_details/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ============================================================
# ======== UPDATE ATTENDANCE RECORD STATUS VIEW TESTS ========
# ============================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsCustomersGroupTest(TestCase):
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

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the attendance record details view
class UpdateAttendanceRecordStatusViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_record_details_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/attendance/attendance/update_attendance_record_status/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ===============================================
# ======== INSTRUCTOR CHOICES VIEW TESTS ========
# ===============================================

# ============== ACCESS PERMISSIONS ==============

# users NOT logged in CANNOT access the instructor choices view
class InstructorChoicesViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the instructor choices view
class InstructorChoicesViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        
        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the instructor choices view
class InstructorChoicesViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the instructor choices view
class InstructorChoicesViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the instructor choices view
class InstructorChoicesViewAsCustomersGroupTest(TestCase):
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

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the instructor choices view
class InstructorChoicesViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the instructor choices view
class InstructorChoicesViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the instructor choices view
class InstructorChoicesViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_instructor_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/instructor_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ==========================================
# ======== EVENT CHOICES VIEW TESTS ========
# ==========================================

# =========== ACCESS PERMISSIONS ===========

# users NOT logged in CANNOT access the event choices view
class EventChoicesViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the event choices view
class EventChoicesViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        
        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the event choices view
class EventChoicesViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the event choices view
class EventChoicesViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the event choices view
class EventChoicesViewAsCustomersGroupTest(TestCase):
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

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the event choices view
class EventChoicesViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the event choices view
class EventChoicesViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the event choices view
class EventChoicesViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_event_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/event_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ============================================
# ======== STUDENT CHOICES VIEW TESTS ========
# ============================================

# ============ ACCESS PERMISSIONS ============

# users NOT logged in CANNOT access the student choices view
class StudentChoicesViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the student choices view
class StudentChoicesViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        
        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the student choices view
class StudentChoicesViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the student choices view
class StudentChoicesViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the student choices view
class StudentChoicesViewAsCustomersGroupTest(TestCase):
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

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the student choices view
class StudentChoicesViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the student choices view
class StudentChoicesViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the student choices view
class StudentChoicesViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_student_choices_view_post(self):
        # attempt to access events all view
        response = self.client.post('/api/attendance/attendance/student_choices/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# =============================================================
# ======== ATTENDANCE USER PREFERENCES VIEW VIEW TESTS ========
# =============================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        
        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewAsCustomersGroupTest(TestCase):
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

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the attendance user preferences view
class AttendanceUserPreferencesViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_attendance_user_preferences_view_get(self):
        # attempt to access attendance user preferences view
        response = self.client.get('/api/attendance/attendance/user_preferences/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# =============================================================
# ======== AUTO GENERATE ATTENDANCE RECORDS VIEW TESTS ========
# =============================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        
        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsCustomersGroupTest(TestCase):
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

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the auto generate attendance records view
class AutoGenerateAttendanceRecordsViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_auto_generate_attendance_records_view_post(self):
        # attempt to access auto generate attendance records view
        response = self.client.post('/api/attendance/attendance/auto_generate_attendance_records/')

# =======================================================
# ======== GET ATTENDANCE FOR PROFILE VIEW TESTS ========
# =======================================================

# ================= ACCESS PERMISSIONS =================

# users NOT logged in CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        
        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Administrators' group
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Displays' group
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsCustomersGroupTest(TestCase):
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

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors' group
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Instructors_Staff' group
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the get attendance for profile view
class GetAttendanceForProfileViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # add user to 'Superusers' group
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_get_attendance_for_profile_view_post(self):
        # attempt to access get attendance for profile view
        response = self.client.post('/api/attendance/attendance/get_attendance_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

