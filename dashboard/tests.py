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