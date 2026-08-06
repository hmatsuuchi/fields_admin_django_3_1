from django.test import TestCase
from django.contrib.auth.models import User, Group
# drf imports
from rest_framework import status
from rest_framework.test import APIClient

# ===============================================================
# ======= INCOMPLETE ATTENDANCE FOR INSTRUCTOR VIEW TESTS =======
# ===============================================================

# ===================== ACCESS PERMISSIONS =====================

# users NOT logged in CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsDisplaysGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Customers' group CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsCustomersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors' group CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsInstructorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the incomplete attendance for instructor view
class IncompleteAttendanceForInstructorViewAsSuperusersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/incomplete_attendance_for_instructor/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ========================================
# ======= STUDENT CHURN VIEW TESTS =======
# ========================================

# ========== ACCESS PERMISSIONS ==========

# users NOT logged in CANNOT access the student churn view
class StudentChurnViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the student churn view
class StudentChurnViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the student churn view
class StudentChurnViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the student churn view
class StudentChurnViewAsDisplaysGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Customers' group CANNOT access the student churn view
class StudentChurnViewAsCustomersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors' group CANNOT access the student churn view
class StudentChurnViewAsInstructorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the student churn view
class StudentChurnViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the student churn view
class StudentChurnViewAsSuperusersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/student_churn/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ================================================
# ======= TOTAL ACTIVE STUDENTS VIEW TESTS =======
# ================================================

# ============== ACCESS PERMISSIONS ==============

# users NOT logged in CANNOT access the total active students view
class TotalActiveStudentsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the total active students view
class TotalActiveStudentsViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the total active students view
class TotalActiveStudentsViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the total active students view
class TotalActiveStudentsViewAsDisplaysGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Customers' group CANNOT access the total active students view
class TotalActiveStudentsViewAsCustomersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors' group CANNOT access the total active students view
class TotalActiveStudentsViewAsInstructorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the total active students view
class TotalActiveStudentsViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the total active students view
class TotalActiveStudentsViewAsSuperusersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ===========================================================
# ======= TOTAL ACTIVE STUDENTS HISTORICAL VIEW TESTS =======
# ===========================================================

# users NOT logged in CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsCustomersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Displays' group CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsDisplaysGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
# users logged in and in the 'Instructors' group CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsInstructorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the total active students historical view
class TotalActiveStudentsHistoricalViewAsSuperusersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/total_active_students_historical/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ===========================================
# ======= AT RISK STUDENTS VIEW TESTS =======
# ===========================================

# =========== ACCESS PERMISSIONS ===========

# users NOT logged in CANNOT access the at risk students view
class AtRiskStudentsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the at risk students view
class AtRiskStudentsViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the at risk students view
class AtRiskStudentsViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the at risk students view
class AtRiskStudentsViewAsDisplaysGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Customers' group CANNOT access the at risk students view
class AtRiskStudentsViewAsCustomersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors' group CANNOT access the at risk students view
class AtRiskStudentsViewAsInstructorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the at risk students view
class AtRiskStudentsViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the at risk students view
class AtRiskStudentsViewAsSuperusersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/at_risk_students/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# =============================================
# ======= UPCOMING BIRTHDAYS VIEW TESTS =======
# =============================================

# ============ ACCESS PERMISSIONS ============

# users NOT logged in CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsDisplaysGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Customers' group CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsCustomersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors' group CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsInstructorsGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the upcoming birthdays view
class UpcomingBirthdaysViewAsSuperusersGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/dashboard/dashboard/upcoming_birthdays/')

# ====================================================================
# ======= TOTAL ACTIVE STUDENTS BY GRADE VIEW TESTS =======
# ====================================================================

# users NOT logged in CANNOT access the total active students by grade view
class TotalActiveStudentsByGradeViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the total active students by grade view
class TotalActiveStudentsByGradeViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TotalActiveStudentsByGradeViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TotalActiveStudentsByGradeViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TotalActiveStudentsByGradeViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TotalActiveStudentsByGradeViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TotalActiveStudentsByGradeViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TotalActiveStudentsByGradeViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/total_active_students_by_grade/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ====================================================================
# ======= REVENUE BY MONTH VIEW TESTS =======
# ====================================================================

class RevenueByMonthViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RevenueByMonthViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueByMonthViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueByMonthViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueByMonthViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueByMonthViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueByMonthViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueByMonthViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ====================================================================
# ======= REVENUE BREAKDOWN BY MONTH VIEW TESTS =======
# ====================================================================

class RevenueBreakdownByMonthViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RevenueBreakdownByMonthViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueBreakdownByMonthViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueBreakdownByMonthViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueBreakdownByMonthViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueBreakdownByMonthViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueBreakdownByMonthViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RevenueBreakdownByMonthViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/revenue_breakdown_by_month/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ====================================================================
# ======= LIFETIME DATA VIEW TESTS =======
# ====================================================================

class LifetimeDataViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class LifetimeDataViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LifetimeDataViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LifetimeDataViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LifetimeDataViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LifetimeDataViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LifetimeDataViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class LifetimeDataViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/lifetime_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ====================================================================
# ======= INSTRUCTOR DATA VIEW TESTS =======
# ====================================================================

class InstructorDataViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InstructorDataViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InstructorDataViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InstructorDataViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InstructorDataViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InstructorDataViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InstructorDataViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InstructorDataViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/instructor_data/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ====================================================================
# ======= CUSTOMER PROFILE DATA VIEW TESTS (Customers Required) =======
# ====================================================================

class CustomerProfileDataViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CustomerProfileDataViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CustomerProfileDataViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CustomerProfileDataViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CustomerProfileDataViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CustomerProfileDataViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CustomerProfileDataViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CustomerProfileDataViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/customer_profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ====================================================================
# ======= INVOICES FOR CUSTOMER VIEW TESTS (Customers Required) =======
# ====================================================================

class InvoicesForCustomerViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InvoicesForCustomerViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForCustomerViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForCustomerViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForCustomerViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForCustomerViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForCustomerViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForCustomerViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/invoices_for_customer/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ====================================================================
# ======= ATTENDANCE FOR ALL INSTRUCTORS VIEW TESTS (Superusers Required) =======
# ====================================================================

class AttendanceForAllInstructorsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AttendanceForAllInstructorsViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AttendanceForAllInstructorsViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AttendanceForAllInstructorsViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AttendanceForAllInstructorsViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AttendanceForAllInstructorsViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AttendanceForAllInstructorsViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AttendanceForAllInstructorsViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/dashboard/dashboard/overview/attendance_for_all_instructors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)