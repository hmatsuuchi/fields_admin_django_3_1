from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from datetime import date

from .models import Students, Phone, PhoneChoice, PrefectureChoices, GradeChoices, StatusChoices, PaymentChoices

# ======= Student Profiles List View Tests =======

# users NOT logged in CANNOT access the student profiles list view
class ProfilesListViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_profiles_list_view(self):
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# users NOT in any group CANNOT access the student profiles list view
class ProfilesListViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_profiles_list_view(self):
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users in the 'Customers' group CANNOT access the student profiles list view
class ProfilesListViewAsCustomerGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Customers')
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_profiles_list_view(self):
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users in the 'Staff' group CAN access the student profiles list view
class ProfilesListViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Staff')
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_profiles_list_view(self):
        response = self.client.get(reverse('student_profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ======= Student Profiles Details View Tests =======
        
# users NOT logged in CANNOT access the student details view using GET, POST, PUT or DELETE
class ProfilesDetailsViewAsUnauthenticatedUserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create test prefecture choice
        test_prefecture_choice = PrefectureChoices()
        test_prefecture_choice.name = 'test_prefecture_choice'
        test_prefecture_choice.order = 1
        test_prefecture_choice.save()  
        # create test phone choice
        test_phone_choice = PhoneChoice()
        test_phone_choice.name = 'test_phone_choice'
        test_phone_choice.order = 1
        test_phone_choice.save()
        # create test phone
        test_phone = Phone()
        test_phone.number = 'test_phone_number'
        test_phone.number_type = test_phone_choice
        test_phone.save()
        # create test grade choice
        test_grade_choice = GradeChoices()
        test_grade_choice.name = 'test_grade_choice'
        test_grade_choice.order = 1
        test_grade_choice.save()
        # create test status choice
        test_status_choice = StatusChoices()
        test_status_choice.name = 'test_status_choice'
        test_status_choice.order = 1
        test_status_choice.save()
        # create test payment choice
        test_payment_choice = PaymentChoices()
        test_payment_choice.name = 'test_payment_choice'
        test_payment_choice.order = 1
        test_payment_choice.save()
        # creates test profile
        test_profile = Students()
        test_profile.save()
        test_profile.last_name_romaji = 'last_name_romaji'
        test_profile.first_name_romaji = 'first_name_romaji'
        test_profile.last_name_kanji = 'last_name_kanji'
        test_profile.first_name_kanji = 'first_name_kanji'
        test_profile.last_name_katakana = 'last_name_katakana'
        test_profile.first_name_katakana = 'first_name_katakana'
        test_profile.post_code = 'post_code'
        test_profile.prefecture = test_prefecture_choice
        test_profile.city = 'city'
        test_profile.address_1 = 'address_1'
        test_profile.address_2 = 'address_2'
        test_profile.phone.add(test_phone)
        test_profile.birthday = date.today()
        test_profile.grade = test_grade_choice
        test_profile.status = test_status_choice
        test_profile.payment_method = test_payment_choice
        test_profile.archived = False
        test_profile.save()
        self.test_profile = test_profile

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': '',
            'first_name_romaji': '',
            'last_name_kanji': '',
            'first_name_kanji': '',
            'last_name_katakana': '',
            'first_name_katakana': '',
            'post_code': '',
            'prefecture': '',
            'city': '',
            'address_1': '',
            'address_2': '',
            'phone': [],
            'birthday': '',
            'grade': '',
            'status': '',
            'payment_method': '',
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
      
# users NOT in any group CANNOT access the student details view using GET, POST, PUT or DELETE
class ProfilesDetailsViewAsNoGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # create test prefecture choice
        test_prefecture_choice = PrefectureChoices()
        test_prefecture_choice.name = 'test_prefecture_choice'
        test_prefecture_choice.order = 1
        test_prefecture_choice.save()  
        # create test phone choice
        test_phone_choice = PhoneChoice()
        test_phone_choice.name = 'test_phone_choice'
        test_phone_choice.order = 1
        test_phone_choice.save()
        # create test phone
        test_phone = Phone()
        test_phone.number = 'test_phone_number'
        test_phone.number_type = test_phone_choice
        test_phone.save()
        # create test grade choice
        test_grade_choice = GradeChoices()
        test_grade_choice.name = 'test_grade_choice'
        test_grade_choice.order = 1
        test_grade_choice.save()
        # create test status choice
        test_status_choice = StatusChoices()
        test_status_choice.name = 'test_status_choice'
        test_status_choice.order = 1
        test_status_choice.save()
        # create test payment choice
        test_payment_choice = PaymentChoices()
        test_payment_choice.name = 'test_payment_choice'
        test_payment_choice.order = 1
        test_payment_choice.save()
        # creates test profile
        test_profile = Students()
        test_profile.save()
        test_profile.last_name_romaji = 'last_name_romaji'
        test_profile.first_name_romaji = 'first_name_romaji'
        test_profile.last_name_kanji = 'last_name_kanji'
        test_profile.first_name_kanji = 'first_name_kanji'
        test_profile.last_name_katakana = 'last_name_katakana'
        test_profile.first_name_katakana = 'first_name_katakana'
        test_profile.post_code = 'post_code'
        test_profile.prefecture = test_prefecture_choice
        test_profile.city = 'city'
        test_profile.address_1 = 'address_1'
        test_profile.address_2 = 'address_2'
        test_profile.phone.add(test_phone)
        test_profile.birthday = date.today()
        test_profile.grade = test_grade_choice
        test_profile.status = test_status_choice
        test_profile.payment_method = test_payment_choice
        test_profile.archived = False
        test_profile.save()
        self.test_profile = test_profile

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': '',
            'first_name_romaji': '',
            'last_name_kanji': '',
            'first_name_kanji': '',
            'last_name_katakana': '',
            'first_name_katakana': '',
            'post_code': '',
            'prefecture': '',
            'city': '',
            'address_1': '',
            'address_2': '',
            'phone': [],
            'birthday': '',
            'grade': '',
            'status': '',
            'payment_method': '',
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users in the 'Customers' group CANNOT access the student details view using GET, POST, PUT or DELETE
class ProfilesDetailsViewAsCustomerGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Customers')
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # create test prefecture choice
        test_prefecture_choice = PrefectureChoices()
        test_prefecture_choice.name = 'test_prefecture_choice'
        test_prefecture_choice.order = 1
        test_prefecture_choice.save()  
        # create test phone choice
        test_phone_choice = PhoneChoice()
        test_phone_choice.name = 'test_phone_choice'
        test_phone_choice.order = 1
        test_phone_choice.save()
        # create test phone
        test_phone = Phone()
        test_phone.number = 'test_phone_number'
        test_phone.number_type = test_phone_choice
        test_phone.save()
        # create test grade choice
        test_grade_choice = GradeChoices()
        test_grade_choice.name = 'test_grade_choice'
        test_grade_choice.order = 1
        test_grade_choice.save()
        # create test status choice
        test_status_choice = StatusChoices()
        test_status_choice.name = 'test_status_choice'
        test_status_choice.order = 1
        test_status_choice.save()
        # create test payment choice
        test_payment_choice = PaymentChoices()
        test_payment_choice.name = 'test_payment_choice'
        test_payment_choice.order = 1
        test_payment_choice.save()
        # creates test profile
        test_profile = Students()
        test_profile.save()
        test_profile.last_name_romaji = 'last_name_romaji'
        test_profile.first_name_romaji = 'first_name_romaji'
        test_profile.last_name_kanji = 'last_name_kanji'
        test_profile.first_name_kanji = 'first_name_kanji'
        test_profile.last_name_katakana = 'last_name_katakana'
        test_profile.first_name_katakana = 'first_name_katakana'
        test_profile.post_code = 'post_code'
        test_profile.prefecture = test_prefecture_choice
        test_profile.city = 'city'
        test_profile.address_1 = 'address_1'
        test_profile.address_2 = 'address_2'
        test_profile.phone.add(test_phone)
        test_profile.birthday = date.today()
        test_profile.grade = test_grade_choice
        test_profile.status = test_status_choice
        test_profile.payment_method = test_payment_choice
        test_profile.archived = False
        test_profile.save()
        self.test_profile = test_profile

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': '',
            'first_name_romaji': '',
            'last_name_kanji': '',
            'first_name_kanji': '',
            'last_name_katakana': '',
            'first_name_katakana': '',
            'post_code': '',
            'prefecture': '',
            'city': '',
            'address_1': '',
            'address_2': '',
            'phone': [],
            'birthday': '',
            'grade': '',
            'status': '',
            'payment_method': '',
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# users in the 'Staff' group CAN access the student details view using GET, POST, PUT or DELETE
class ProfilesDetailsViewAsStaffGroupTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Staff')
        self.user.groups.add(self.group)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # create test prefecture choice
        test_prefecture_choice = PrefectureChoices()
        test_prefecture_choice.name = 'test_prefecture_choice'
        test_prefecture_choice.order = 1
        test_prefecture_choice.save()  
        # create test phone choice
        test_phone_choice = PhoneChoice()
        test_phone_choice.name = 'test_phone_choice'
        test_phone_choice.order = 1
        test_phone_choice.save()
        # create test phone
        test_phone = Phone()
        test_phone.number = 'test_phone_number'
        test_phone.number_type = test_phone_choice
        test_phone.save()
        # create test grade choice
        test_grade_choice = GradeChoices()
        test_grade_choice.name = 'test_grade_choice'
        test_grade_choice.order = 1
        test_grade_choice.save()
        # create test status choice
        test_status_choice = StatusChoices()
        test_status_choice.name = 'test_status_choice'
        test_status_choice.order = 1
        test_status_choice.save()
        # create test payment choice
        test_payment_choice = PaymentChoices()
        test_payment_choice.name = 'test_payment_choice'
        test_payment_choice.order = 1
        test_payment_choice.save()
        # creates test profile
        test_profile = Students()
        test_profile.save()
        test_profile.last_name_romaji = 'last_name_romaji'
        test_profile.first_name_romaji = 'first_name_romaji'
        test_profile.last_name_kanji = 'last_name_kanji'
        test_profile.first_name_kanji = 'first_name_kanji'
        test_profile.last_name_katakana = 'last_name_katakana'
        test_profile.first_name_katakana = 'first_name_katakana'
        test_profile.post_code = 'post_code'
        test_profile.prefecture = test_prefecture_choice
        test_profile.city = 'city'
        test_profile.address_1 = 'address_1'
        test_profile.address_2 = 'address_2'
        test_profile.phone.add(test_phone)
        test_profile.birthday = date.today()
        test_profile.grade = test_grade_choice
        test_profile.status = test_status_choice
        test_profile.payment_method = test_payment_choice
        test_profile.archived = False
        test_profile.save()
        self.test_profile = test_profile

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': '',
            'first_name_romaji': '',
            'last_name_kanji': '',
            'first_name_kanji': '',
            'last_name_katakana': '',
            'first_name_katakana': '',
            'post_code': '',
            'prefecture': '',
            'city': '',
            'address_1': '',
            'address_2': '',
            'phone': [],
            'birthday': '',
            'grade': '',
            'status': '',
            'payment_method': '',
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)