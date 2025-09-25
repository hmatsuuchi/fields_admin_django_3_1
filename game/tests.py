from django.test import TestCase
from django.contrib.auth.models import User, Group
# drf imports
from rest_framework import status
from rest_framework.test import APIClient

# ===========================================
# ======= GET STUDENT DATA VIEW TESTS =======
# ===========================================

# =========== ACCESS PERMISSIONS ===========

# users NOT logged in CANNOT access the get student data view
class GetStudentDataViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the get student data view
class GetStudentDataViewAsAsNoGroupUserTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the get student data view
class GetStudentDataViewAsAdministratorsGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Customers' group CANNOT access the get student data view
class GetStudentDataViewAsCustomersGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors' group CANNOT access the get student data view
class GetStudentDataViewAsInstructorsGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the get student data view
class GetStudentDataViewAsInstructorsStaffGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CANNOT access the get student data view
class GetStudentDataViewAsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the get student data view
class GetStudentDataViewAsSuperusersGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_student_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ==============================================
# ======= GET RECENT CHECKINS VIEW TESTS =======
# ==============================================

# ============= ACCESS PERMISSIONS =============

# users NOT logged in CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsAsNoGroupUserTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsAdministratorsGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Customers' group CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsCustomersGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors' group CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsInstructorsGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Instructors_Staff' group CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsInstructorsStaffGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsStaffGroupTest(TestCase):
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

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Superusers' group CANNOT access the get recent checkins view
class GetRecentCheckinsViewAsSuperusersGroupTest(TestCase):
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
        response = self.client.get('/api/game/display/01/get_recent_checkins/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)