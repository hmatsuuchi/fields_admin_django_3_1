from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APIClient

# ================================================
# ======= INVOICE LIST ALL VIEW TESTS =======
# ================================================

# =========== ACCESS PERMISSIONS ===========

class InvoiceListAllViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InvoiceListAllViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceListAllViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceListAllViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceListAllViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceListAllViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceListAllViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceListAllViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceListAllViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/list/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ================================================
# ======= INVOICE STATUS ALL VIEW TESTS =======
# ================================================

class InvoiceStatusAllViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InvoiceStatusAllViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusAllViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusAllViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusAllViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusAllViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusAllViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusAllViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusAllViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/status/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ================================================
# ======= INVOICE STATUS BATCH UPDATE VIEW TESTS =======
# ================================================

class InvoiceStatusBatchUpdateViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InvoiceStatusBatchUpdateViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusBatchUpdateViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusBatchUpdateViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusBatchUpdateViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusBatchUpdateViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusBatchUpdateViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusBatchUpdateViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceStatusBatchUpdateViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/status/batch-update/', data=[], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ================================================
# ======= INVOICE CREATE VIEW TESTS =======
# ================================================

class InvoiceCreateViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InvoiceCreateViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceCreateViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceCreateViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceCreateViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceCreateViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceCreateViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceCreateViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoiceCreateViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_post(self):
        response = self.client.post('/api/invoices/invoices/create/invoice/', data={})
        # Will return 400 due to validation errors, but permission passed
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

# ================================================
# ======= INVOICE PRINT VIEW TESTS =======
# ================================================

class InvoicePrintViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InvoicePrintViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicePrintViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicePrintViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicePrintViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicePrintViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicePrintViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicePrintViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicePrintViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/print/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

# ================================================
# ======= PROFILES LIST FOR SELECT VIEW TESTS =======
# ================================================

class ProfilesListForSelectViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProfilesListForSelectViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfilesListForSelectViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfilesListForSelectViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfilesListForSelectViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfilesListForSelectViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfilesListForSelectViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfilesListForSelectViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ProfilesListForSelectViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/profiles-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ================================================
# ======= PAYMENT METHODS LIST FOR SELECT VIEW TESTS =======
# ================================================

class PaymentMethodsListForSelectViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PaymentMethodsListForSelectViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PaymentMethodsListForSelectViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PaymentMethodsListForSelectViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PaymentMethodsListForSelectViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PaymentMethodsListForSelectViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PaymentMethodsListForSelectViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PaymentMethodsListForSelectViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class PaymentMethodsListForSelectViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/payment-methods-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ================================================
# ======= SERVICE TYPES LIST FOR SELECT VIEW TESTS =======
# ================================================

class ServiceTypesListForSelectViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ServiceTypesListForSelectViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ServiceTypesListForSelectViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ServiceTypesListForSelectViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ServiceTypesListForSelectViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ServiceTypesListForSelectViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ServiceTypesListForSelectViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ServiceTypesListForSelectViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ServiceTypesListForSelectViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/service-types-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ================================================
# ======= TAXES LIST FOR SELECT VIEW TESTS =======
# ================================================

class TaxesListForSelectViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TaxesListForSelectViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaxesListForSelectViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaxesListForSelectViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaxesListForSelectViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaxesListForSelectViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaxesListForSelectViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaxesListForSelectViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TaxesListForSelectViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/taxes-list-for-select/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ================================================
# ======= INVOICES FOR STUDENT FOR INVOICE VIEW TESTS =======
# ================================================

class InvoicesForStudentForInvoiceViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class InvoicesForStudentForInvoiceViewAsNoGroupUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForStudentForInvoiceViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForStudentForInvoiceViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForStudentForInvoiceViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForStudentForInvoiceViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForStudentForInvoiceViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForStudentForInvoiceViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class InvoicesForStudentForInvoiceViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_view_get(self):
        response = self.client.get('/api/invoices/invoices/invoices_for_student_for_invoice_create/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
