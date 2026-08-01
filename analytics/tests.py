from django.test import TestCase
# django imports
from django.contrib.auth.models import User, Group
from django.test import override_settings
# drf imports
from rest_framework import status
from rest_framework.test import APIClient

# ============================================================
# ======== STUDENT CHURN MODEL TRAIN VIEW TESTS ==============
# ============================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the student churn model train view
class StudentChurnModelTrainViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_student_churn_model_train_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_model_train/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in but NOT in any group CANNOT access the student churn model train view
class StudentChurnModelTrainViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_student_churn_model_train_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_model_train/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in and in the 'Staff' group CANNOT access the student churn model train view
class StudentChurnModelTrainViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_student_churn_model_train_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_model_train/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in but in the 'Administrators' group CANNOT access the student churn model train view
class StudentChurnModelTrainViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_student_churn_model_train_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_model_train/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in but in the 'Superusers' group CANNOT access in production
class StudentChurnModelTrainViewAsSuperusersGroupProductionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    @override_settings(DEBUG=False)
    def test_student_churn_model_train_view_get_production(self):
        response = self.client.get('/api/analytics/analytics/student_churn_model_train/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ============================================================
# ======== STUDENT CHURN PREDICT VIEW TESTS ==================
# ============================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the student churn predict view
class StudentChurnPredictViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_student_churn_predict_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_predict/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in but NOT in any group CANNOT access the student churn predict view
class StudentChurnPredictViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_student_churn_predict_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_predict/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in and in the 'Staff' group CANNOT access the student churn predict view
class StudentChurnPredictViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_student_churn_predict_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_predict/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in but in the 'Administrators' group CANNOT access the student churn predict view
class StudentChurnPredictViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_student_churn_predict_view_get(self):
        response = self.client.get('/api/analytics/analytics/student_churn_predict/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# users logged in but in the 'Superusers' group CANNOT access in production
class StudentChurnPredictViewAsSuperusersGroupProductionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    @override_settings(DEBUG=False)
    def test_student_churn_predict_view_get_production(self):
        response = self.client.get('/api/analytics/analytics/student_churn_predict/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

