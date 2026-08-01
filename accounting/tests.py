from django.test import TestCase
# django imports
from django.contrib.auth.models import User, Group
# drf imports
from rest_framework import status
from rest_framework.test import APIClient


# ================================================================
# ======== JOURNAL ENTRIES CREATE VIEW TESTS =====================
# ================================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the journal entries create view
class JournalEntriesCreateViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the journal entries create view
class JournalEntriesCreateViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the journal entries create view
class JournalEntriesCreateViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the journal entries create view
class JournalEntriesCreateViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the journal entries create view
class JournalEntriesCreateViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the journal entries create view
class JournalEntriesCreateViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the journal entries create view
class JournalEntriesCreateViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the journal entries create view
class JournalEntriesCreateViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the journal entries create view
class JournalEntriesCreateViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_journal_entries_create_view_post(self):
        response = self.client.post('/api/accounting/accounting/journal_entries/create/')
        # Empty POST should return 400 (bad request) not 403, but not 401
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])


# ================================================================
# ======== ACCOUNT LIST FOR DROPDOWN MENU VIEW TESTS =============
# ================================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the account list view
class AccountListForDropdownMenuViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the account list view
class AccountListForDropdownMenuViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the account list view
class AccountListForDropdownMenuViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the account list view
class AccountListForDropdownMenuViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the account list view
class AccountListForDropdownMenuViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the account list view
class AccountListForDropdownMenuViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the account list view
class AccountListForDropdownMenuViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the account list view
class AccountListForDropdownMenuViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the account list view
class AccountListForDropdownMenuViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_account_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ================================================================
# ======== CONTACT LIST FOR DROPDOWN MENU VIEW TESTS =============
# ================================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the contact list view
class ContactListForDropdownMenuViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the contact list view
class ContactListForDropdownMenuViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the contact list view
class ContactListForDropdownMenuViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the contact list view
class ContactListForDropdownMenuViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the contact list view
class ContactListForDropdownMenuViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the contact list view
class ContactListForDropdownMenuViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the contact list view
class ContactListForDropdownMenuViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the contact list view
class ContactListForDropdownMenuViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the contact list view
class ContactListForDropdownMenuViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_contact_list_view_get(self):
        response = self.client.get('/api/accounting/accounting/contacts/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ================================================================
# ======== BALANCE SHEET VIEW TESTS ==============================
# ================================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the balance sheet view
class BalanceSheetViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the balance sheet view
class BalanceSheetViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the balance sheet view
class BalanceSheetViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the balance sheet view
class BalanceSheetViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the balance sheet view
class BalanceSheetViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the balance sheet view
class BalanceSheetViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the balance sheet view
class BalanceSheetViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the balance sheet view
class BalanceSheetViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the balance sheet view
class BalanceSheetViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_balance_sheet_view_get(self):
        response = self.client.get('/api/accounting/accounting/accounts/balance_sheet/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ================================================================
# ======== ACCOUNT ACTIVITY VIEW TESTS ===========================
# ================================================================

# ==================== ACCESS PERMISSIONS ====================

# users NOT logged in CANNOT access the account activity view
class AccountActivityViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users logged in but NOT in any group CANNOT access the account activity view
class AccountActivityViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Administrators' group CANNOT access the account activity view
class AccountActivityViewAsAdministratorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        administrators_group = Group.objects.create(name='Administrators')
        self.user.groups.add(administrators_group)
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Displays' group CANNOT access the account activity view
class AccountActivityViewAsDisplaysGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        displays_group = Group.objects.create(name='Displays')
        self.user.groups.add(displays_group)
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Customers' group CANNOT access the account activity view
class AccountActivityViewAsCustomersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        customers_group = Group.objects.create(name='Customers')
        self.user.groups.add(customers_group)
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors' group CANNOT access the account activity view
class AccountActivityViewAsInstructorsGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_group = Group.objects.create(name='Instructors')
        self.user.groups.add(instructors_group)
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Instructors_Staff' group CANNOT access the account activity view
class AccountActivityViewAsInstructorsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        instructors_staff_group = Group.objects.create(name='Instructors_Staff')
        self.user.groups.add(instructors_staff_group)
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in but in the 'Superusers' group CANNOT access the account activity view
class AccountActivityViewAsSuperusersGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        superusers_group = Group.objects.create(name='Superusers')
        self.user.groups.add(superusers_group)
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users logged in and in the 'Staff' group CAN access the account activity view (but may get 400 without account_id param)
class AccountActivityViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        staff_group = Group.objects.create(name='Staff')
        self.user.groups.add(staff_group)
        self.client.force_authenticate(user=self.user)

    def test_account_activity_view_get(self):
        response = self.client.get('/api/accounting/accounting/account/transactions/')
        # Missing account_id parameter should return 400, not 403
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK])
