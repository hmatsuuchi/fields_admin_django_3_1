from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse
import json
# drf imports
from rest_framework import status
from rest_framework.test import APIClient

# ==================================================
# ======= GET JOURNAL FOR PROFILE VIEW TESTS =======
# ==================================================

# =============== ACCESS PERMISSIONS ===============

# users NOT logged in CANNOT access the get journal for profile view
class GetJournalForProfileViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the get journal for profile view
class GetJournalForProfileViewAsAsNoGroupUserTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the get journal for profile view
class GetJournalForProfileViewAsAdministratorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the get journal for profile view
class GetJournalForProfileViewAsCustomersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the get journal for profile view
class GetJournalForProfileViewAsDisplaysGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the get journal for profile view
class GetJournalForProfileViewAsInstructorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the get journal for profile view
class GetJournalForProfileViewAsInstructorsStaffGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the get journal for profile view
class GetJournalForProfileViewAsSuperusersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_for_profile/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ============================================
# ======= GET JOURNAL TYPES VIEW TESTS =======
# ============================================

# ============ ACCESS PERMISSIONS ============

# users NOT logged in CANNOT access the get journal types view
class GetJournalTypesViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the get journal types view
class GetJournalTypesViewAsNoGroupUserTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the get journal types view
class GetJournalTypesViewAsAdministratorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the get journal types view
class GetJournalTypesViewAsCustomersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the get journal types view
class GetJournalTypesViewAsDisplaysGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the get journal types view
class GetJournalTypesViewAsInstructorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the get journal types view
class GetJournalTypesViewAsInstructorsStaffGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the get journal types view
class GetJournalTypesViewAsSuperusersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_journal_types/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# =================================================
# ======= GET ACTIVE INSTRUCTORS VIEW TESTS =======
# =================================================

# ============== ACCESS PERMISSIONS ==============

# users NOT logged in CANNOT access the get active instructors view
class GetActiveInstructorsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the get active instructors view
class GetActiveInstructorsViewAsNoGroupUserTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the get active instructors view
class GetActiveInstructorsViewAsAdministratorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the get active instructors view
class GetActiveInstructorsViewAsCustomersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the get active instructors view
class GetActiveInstructorsViewAsDisplaysGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the get active instructors view
class GetActiveInstructorsViewAsInstructorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the get active instructors view
class GetActiveInstructorsViewAsInstructorsStaffGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the get active instructors view
class GetActiveInstructorsViewAsSuperusersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_active_instructors/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ===========================================
# ======= GET PROFILE DATA VIEW TESTS =======
# ===========================================

# =========== ACCESS PERMISSIONS ===========

# users NOT logged in CANNOT access the get profile data view
class GetProfileDataViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_get(self):
        # attempt to access view
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the get profile data view
class GetProfileDataViewAsNoGroupUserTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the get profile data view
class GetProfileDataViewAsAdministratorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the get profile data view
class GetProfileDataViewAsCustomersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the get profile data view
class GetProfileDataViewAsDisplaysGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the get profile data view
class GetProfileDataViewAsInstructorsGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the get profile data view
class GetProfileDataViewAsInstructorsStaffGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the get profile data view
class GetProfileDataViewAsSuperusersGroupTest(TestCase):
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
        response = self.client.get('/api/journal/journal/get_profile_data/')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ===============================================
# ======= CREATE JOURNAL ENTRY VIEW TESTS =======
# ===============================================

# ============= ACCESS PERMISSIONS =============

# users NOT logged in CANNOT access the create journal entry view
class CreateJournalEntryViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the create journal entry view
class CreateJournalEntryViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the create journal entry view
class CreateJournalEntryViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the create journal entry view
class CreateJournalEntryViewAsCustomersGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the create journal entry view
class CreateJournalEntryViewAsDisplaysGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the create journal entry view
class CreateJournalEntryViewAsInstructorsGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the create journal entry view
class CreateJournalEntryViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the create journal entry view
class CreateJournalEntryViewAsSuperusersGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'student': '999',
            'date': '2025-01-01',
            'time': '12:00:00',
            'type': '999',
            'instructor': '999',
            'text': 'This is a test journal entry.',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to create new journal entry
        response = self.client.post(reverse('create_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# ================================================
# ======= ARCHIVE JOURNAL ENTRY VIEW TESTS =======
# ================================================

# ============== ACCESS PERMISSIONS ==============

# users NOT logged in CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 401 UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        # create test client
        self.client = APIClient()

        # create user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsAdministratorsGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsCustomersGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsDisplaysGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsInstructorsGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsInstructorsStaffGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the archive journal entry view
class ArchiveJournalEntryViewAsSuperusersGroupTest(TestCase):
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

    def test_view_post(self):
        # journal entry data
        data = {
            'journal_id': '999',
            }

        # converts journal entry data to json
        json_data = json.dumps(data)

        # attempt to archive journal entry
        response = self.client.put(reverse('archive_journal_entry'), json_data, content_type='application/json')

        # response status code is 403 FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

