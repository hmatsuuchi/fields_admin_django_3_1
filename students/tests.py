from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
import json
from datetime import date, timedelta

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
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': 'last_name_romaji',
            'first_name_romaji': 'first_name_romaji',
            'last_name_kanji': 'last_name_kanji',
            'first_name_kanji': 'first_name_kanji',
            'last_name_katakana': 'last_name_katakana',
            'first_name_katakana': 'first_name_katakana',
            'post_code': '123-4567',
            'prefecture': self.test_prefecture_choice.id,
            'city': 'city',
            'address_1': 'address_1',
            'address_2': 'address_2',
            'phone': [{'number': '123-456-7890', 'number_type': self.test_phone_choice.id}],
            'birthday': (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice.id,
            'status': self.test_status_choice.id,
            'payment_method': self.test_payment_choice.id,
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PUT - update a student profile
    def test_profiles_details_view_put(self):
        data = {
            'profile_id': self.test_profile.id,
            'last_name_romaji': 'last_name_romaji_updated',
            'first_name_romaji': 'first_name_romaji_updated',
            'last_name_kanji': 'last_name_kanji_updated',
            'first_name_kanji': 'first_name_kanji_updated',
            'last_name_katakana': 'last_name_katakana_updated',
            'first_name_katakana': 'first_name_katakana_updated',
            'post_code': '765-4321',
            'prefecture': self.test_prefecture_choice_updated.id,
            'city': 'city_updated',
            'address_1': 'address_1_updated',
            'address_2': 'address_2_updated',
            'phone': [{'number': '098-765-4321', 'number_type': self.test_phone_choice_updated.id}],
            'birthday': (date.today() - timedelta(days=(365*10))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice_updated.id,
            'status': self.test_status_choice_updated.id,
            'payment_method': self.test_payment_choice_updated.id,
            'archived': True,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.put(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE - delete a student profile
    def test_profiles_details_view_delete(self):
        response = self.client.delete(f"{reverse('student_profiles_details')}?profile_id={self.test_profile.id}")
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
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': 'last_name_romaji',
            'first_name_romaji': 'first_name_romaji',
            'last_name_kanji': 'last_name_kanji',
            'first_name_kanji': 'first_name_kanji',
            'last_name_katakana': 'last_name_katakana',
            'first_name_katakana': 'first_name_katakana',
            'post_code': '123-4567',
            'prefecture': self.test_prefecture_choice.id,
            'city': 'city',
            'address_1': 'address_1',
            'address_2': 'address_2',
            'phone': [{'number': '123-456-7890', 'number_type': self.test_phone_choice.id}],
            'birthday': (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice.id,
            'status': self.test_status_choice.id,
            'payment_method': self.test_payment_choice.id,
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # PUT - update a student profile
    def test_profiles_details_view_put(self):
        data = {
            'profile_id': self.test_profile.id,
            'last_name_romaji': 'last_name_romaji_updated',
            'first_name_romaji': 'first_name_romaji_updated',
            'last_name_kanji': 'last_name_kanji_updated',
            'first_name_kanji': 'first_name_kanji_updated',
            'last_name_katakana': 'last_name_katakana_updated',
            'first_name_katakana': 'first_name_katakana_updated',
            'post_code': '765-4321',
            'prefecture': self.test_prefecture_choice_updated.id,
            'city': 'city_updated',
            'address_1': 'address_1_updated',
            'address_2': 'address_2_updated',
            'phone': [{'number': '098-765-4321', 'number_type': self.test_phone_choice_updated.id}],
            'birthday': (date.today() - timedelta(days=(365*10))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice_updated.id,
            'status': self.test_status_choice_updated.id,
            'payment_method': self.test_payment_choice_updated.id,
            'archived': True,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.put(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE - delete a student profile
    def test_profiles_details_view_delete(self):
        response = self.client.delete(f"{reverse('student_profiles_details')}?profile_id={self.test_profile.id}")
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
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': 'last_name_romaji',
            'first_name_romaji': 'first_name_romaji',
            'last_name_kanji': 'last_name_kanji',
            'first_name_kanji': 'first_name_kanji',
            'last_name_katakana': 'last_name_katakana',
            'first_name_katakana': 'first_name_katakana',
            'post_code': '123-4567',
            'prefecture': self.test_prefecture_choice.id,
            'city': 'city',
            'address_1': 'address_1',
            'address_2': 'address_2',
            'phone': [{'number': '123-456-7890', 'number_type': self.test_phone_choice.id}],
            'birthday': (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice.id,
            'status': self.test_status_choice.id,
            'payment_method': self.test_payment_choice.id,
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # PUT - update a student profile
    def test_profiles_details_view_put(self):
        data = {
            'profile_id': self.test_profile.id,
            'last_name_romaji': 'last_name_romaji_updated',
            'first_name_romaji': 'first_name_romaji_updated',
            'last_name_kanji': 'last_name_kanji_updated',
            'first_name_kanji': 'first_name_kanji_updated',
            'last_name_katakana': 'last_name_katakana_updated',
            'first_name_katakana': 'first_name_katakana_updated',
            'post_code': '765-4321',
            'prefecture': self.test_prefecture_choice_updated.id,
            'city': 'city_updated',
            'address_1': 'address_1_updated',
            'address_2': 'address_2_updated',
            'phone': [{'number': '098-765-4321', 'number_type': self.test_phone_choice_updated.id}],
            'birthday': (date.today() - timedelta(days=(365*10))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice_updated.id,
            'status': self.test_status_choice_updated.id,
            'payment_method': self.test_payment_choice_updated.id,
            'archived': True,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.put(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # DELETE - delete a student profile
    def test_profiles_details_view_delete(self):
        response = self.client.delete(f"{reverse('student_profiles_details')}?profile_id={self.test_profile.id}")
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
        self.test_prefecture_choice = PrefectureChoices()
        self.test_prefecture_choice.name = 'test_prefecture_choice'
        self.test_prefecture_choice.order = 1
        self.test_prefecture_choice.save()
        self.test_prefecture_choice_updated = PrefectureChoices()
        self.test_prefecture_choice_updated.name = 'test_prefecture_choice_updated'
        self.test_prefecture_choice_updated.order = 2
        self.test_prefecture_choice_updated.save()
        # create test phone choice
        self.test_phone_choice = PhoneChoice()
        self.test_phone_choice.name = 'test_phone_choice'
        self.test_phone_choice.order = 1
        self.test_phone_choice.save()
        self.test_phone_choice_updated = PhoneChoice()
        self.test_phone_choice_updated.name = 'test_phone_choice_updated'
        self.test_phone_choice_updated.order = 2
        self.test_phone_choice_updated.save()
        # create test phone
        self.test_phone = Phone()
        self.test_phone.number = '123-456-7890'
        self.test_phone.number_type = self.test_phone_choice
        self.test_phone.save()
        self.test_phone_updated = Phone()
        self.test_phone_updated.number = '098-765-4321'
        self.test_phone_updated.number_type = self.test_phone_choice_updated
        self.test_phone_updated.save()
        # create test grade choice
        self.test_grade_choice = GradeChoices()
        self.test_grade_choice.name = 'test_grade_choice'
        self.test_grade_choice.order = 1
        self.test_grade_choice.save()
        self.test_grade_choice_updated = GradeChoices()
        self.test_grade_choice_updated.name = 'test_grade_choice_updated'
        self.test_grade_choice_updated.order = 2
        self.test_grade_choice_updated.save()
        # create test status choice
        self.test_status_choice = StatusChoices()
        self.test_status_choice.name = 'test_status_choice'
        self.test_status_choice.order = 1
        self.test_status_choice.save()
        self.test_status_choice_updated = StatusChoices()
        self.test_status_choice_updated.name = 'test_status_choice_updated'
        self.test_status_choice_updated.order = 2
        self.test_status_choice_updated.save()
        # create test payment choice
        self.test_payment_choice = PaymentChoices()
        self.test_payment_choice.name = 'test_payment_choice'
        self.test_payment_choice.order = 1
        self.test_payment_choice.save()
        self.test_payment_choice_updated = PaymentChoices()
        self.test_payment_choice_updated.name = 'test_payment_choice_updated'
        self.test_payment_choice_updated.order = 1
        self.test_payment_choice_updated.save()
        # creates test profile
        self.test_profile = Students()
        self.test_profile.save()
        self.test_profile.last_name_romaji = 'last_name_romaji'
        self.test_profile.first_name_romaji = 'first_name_romaji'
        self.test_profile.last_name_kanji = 'last_name_kanji'
        self.test_profile.first_name_kanji = 'first_name_kanji'
        self.test_profile.last_name_katakana = 'last_name_katakana'
        self.test_profile.first_name_katakana = 'first_name_katakana'
        self.test_profile.post_code = '123-4567'
        self.test_profile.prefecture = self.test_prefecture_choice
        self.test_profile.city = 'city'
        self.test_profile.address_1 = 'address_1'
        self.test_profile.address_2 = 'address_2'
        self.test_profile.phone.add(self.test_phone)
        self.test_profile.birthday = (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d')
        self.test_profile.grade = self.test_grade_choice
        self.test_profile.status = self.test_status_choice
        self.test_profile.payment_method = self.test_payment_choice
        self.test_profile.archived = False
        self.test_profile.save()

    # GET - retrieve a student profile
    def test_profiles_details_view_get(self):
        params = {'profile_id': self.test_profile.id}

        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name_romaji'], 'last_name_romaji')
        self.assertEqual(response.data['first_name_romaji'], 'first_name_romaji')
        self.assertEqual(response.data['last_name_kanji'], 'last_name_kanji')
        self.assertEqual(response.data['first_name_kanji'], 'first_name_kanji')
        self.assertEqual(response.data['last_name_katakana'], 'last_name_katakana')
        self.assertEqual(response.data['first_name_katakana'], 'first_name_katakana')
        self.assertEqual(response.data['post_code'], '123-4567')
        self.assertEqual(response.data['prefecture'], self.test_profile.prefecture.id)
        self.assertEqual(response.data['city'], 'city')
        self.assertEqual(response.data['address_1'], 'address_1')
        self.assertEqual(response.data['address_2'], 'address_2')
        self.assertEqual(response.data['phone'][0]['number'], '123-456-7890')
        self.assertEqual(response.data['phone'][0]['number_type'], self.test_phone_choice.id)
        self.assertEqual(response.data['birthday'], (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d'))
        self.assertEqual(response.data['grade'], self.test_grade_choice.id)
        self.assertEqual(response.data['status'], self.test_status_choice.id)
        self.assertEqual(response.data['payment_method'], self.test_payment_choice.id)
        self.assertEqual(response.data['archived'], False)

    # POST - create a new student profile
    def test_profiles_details_view_post(self):
        data = {
            'last_name_romaji': 'last_name_romaji',
            'first_name_romaji': 'first_name_romaji',
            'last_name_kanji': 'last_name_kanji',
            'first_name_kanji': 'first_name_kanji',
            'last_name_katakana': 'last_name_katakana',
            'first_name_katakana': 'first_name_katakana',
            'post_code': '123-4567',
            'prefecture': self.test_prefecture_choice.id,
            'city': 'city',
            'address_1': 'address_1',
            'address_2': 'address_2',
            'phone': [{'number': '123-456-7890', 'number_type': self.test_phone_choice.id}],
            'birthday': (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice.id,
            'status': self.test_status_choice.id,
            'payment_method': self.test_payment_choice.id,
            'archived': False,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.post(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['last_name_romaji'], 'last_name_romaji')
        self.assertEqual(response.data['first_name_romaji'], 'first_name_romaji')
        self.assertEqual(response.data['last_name_kanji'], 'last_name_kanji')
        self.assertEqual(response.data['first_name_kanji'], 'first_name_kanji')
        self.assertEqual(response.data['last_name_katakana'], 'last_name_katakana')
        self.assertEqual(response.data['first_name_katakana'], 'first_name_katakana')
        self.assertEqual(response.data['post_code'], '123-4567')
        self.assertEqual(response.data['prefecture'], self.test_prefecture_choice.id)
        self.assertEqual(response.data['city'], 'city')
        self.assertEqual(response.data['address_1'], 'address_1')
        self.assertEqual(response.data['address_2'], 'address_2')
        self.assertEqual(response.data['phone'][0]['number'], '123-456-7890')
        self.assertEqual(response.data['phone'][0]['number_type'], self.test_phone_choice.id)
        self.assertEqual(response.data['birthday'], (date.today() - timedelta(days=(365*9))).strftime('%Y-%m-%d'))
        self.assertEqual(response.data['grade'], self.test_grade_choice.id)
        self.assertEqual(response.data['status'], self.test_status_choice.id)
        self.assertEqual(response.data['payment_method'], self.test_payment_choice.id)
        self.assertEqual(response.data['archived'], False)

    # PUT - update a student profile
    def test_profiles_details_view_put(self):
        data = {
            'profile_id': self.test_profile.id,
            'last_name_romaji': 'last_name_romaji_updated',
            'first_name_romaji': 'first_name_romaji_updated',
            'last_name_kanji': 'last_name_kanji_updated',
            'first_name_kanji': 'first_name_kanji_updated',
            'last_name_katakana': 'last_name_katakana_updated',
            'first_name_katakana': 'first_name_katakana_updated',
            'post_code': '765-4321',
            'prefecture': self.test_prefecture_choice_updated.id,
            'city': 'city_updated',
            'address_1': 'address_1_updated',
            'address_2': 'address_2_updated',
            'phone': [{'number': '098-765-4321', 'number_type': self.test_phone_choice_updated.id}],
            'birthday': (date.today() - timedelta(days=(365*10))).strftime('%Y-%m-%d'),
            'grade': self.test_grade_choice_updated.id,
            'status': self.test_status_choice_updated.id,
            'payment_method': self.test_payment_choice_updated.id,
            'archived': True,
            }
        
        json_data = json.dumps(data)
                    
        response = self.client.put(reverse('student_profiles_details'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['last_name_romaji'], 'last_name_romaji_updated')
        self.assertEqual(response.data['first_name_romaji'], 'first_name_romaji_updated')
        self.assertEqual(response.data['last_name_kanji'], 'last_name_kanji_updated')
        self.assertEqual(response.data['first_name_kanji'], 'first_name_kanji_updated')
        self.assertEqual(response.data['last_name_katakana'], 'last_name_katakana_updated')
        self.assertEqual(response.data['first_name_katakana'], 'first_name_katakana_updated')
        self.assertEqual(response.data['post_code'], '765-4321')
        self.assertEqual(response.data['prefecture'], self.test_prefecture_choice_updated.id)
        self.assertEqual(response.data['city'], 'city_updated')
        self.assertEqual(response.data['address_1'], 'address_1_updated')
        self.assertEqual(response.data['address_2'], 'address_2_updated')
        self.assertEqual(response.data['phone'][0]['number'], '098-765-4321')
        self.assertEqual(response.data['phone'][0]['number_type'], self.test_phone_choice_updated.id)
        self.assertEqual(response.data['birthday'], (date.today() - timedelta(days=(365*10))).strftime('%Y-%m-%d'))
        self.assertEqual(response.data['grade'], self.test_grade_choice_updated.id)
        self.assertEqual(response.data['status'], self.test_status_choice_updated.id)
        self.assertEqual(response.data['payment_method'], self.test_payment_choice_updated.id)
        self.assertEqual(response.data['archived'], True)

    # DELETE - delete a student profile
    def test_profiles_details_view_delete(self):
        response = self.client.delete(f"{reverse('student_profiles_details')}?profile_id={self.test_profile.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        params = {'profile_id': self.test_profile.id}
        response = self.client.get(reverse('student_profiles_details'), params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)