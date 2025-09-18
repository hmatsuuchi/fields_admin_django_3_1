from django.test import TestCase
# django imports
from django.contrib.auth.models import User, Group
# drf imports
from rest_framework import status
from rest_framework.test import APIClient


# ======= STUDEN CHURN MODEL PREDICT FOR ATTENDANCE RECORD - ACCESS PERMISSIONS =======

# users NOT logged in CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_attendance_for_date_view_get(self):
        # attempt to access events all view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsNoGroupTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_student_churn_model_predict_for_attendance_view_get(self):
        # attempt to access student churn model predict for attendance view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsAdministratorsGroupTest(TestCase):
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

    def test_student_churn_model_predict_for_attendance_view_get(self):
        # attempt to access student churn model predict for attendance view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsDisplaysGroupTest(TestCase):
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

    def test_student_churn_model_predict_for_attendance_view_get(self):
        # attempt to access student churn model predict for attendance view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsCustomersGroupTest(TestCase):
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

    def test_student_churn_model_predict_for_attendance_view_get(self):
        # attempt to access student churn model predict for attendance view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsInstructorsGroupTest(TestCase):
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

    def test_student_churn_model_predict_for_attendance_view_get(self):
        # attempt to access student churn model predict for attendance view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_student_churn_model_predict_for_attendance_view_get(self):
        # attempt to access student churn model predict for attendance view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the student churn model predict for attendance view
class StudentChurnModelPredictForAttendanceRecordViewAsSuperusersGroupTest(TestCase):
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

    def test_student_churn_model_predict_for_attendance_view_get(self):
        # attempt to access student churn model predict for attendance view
        response = self.client.get('/api/analytics/analytics/ml_predict_for_attendance_record/999/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)