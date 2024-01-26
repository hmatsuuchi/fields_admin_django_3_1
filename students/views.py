from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import PaymentChoices, Phone, PhoneChoice, GradeChoices, StatusChoices, PrefectureChoices
from .models import Students
from .serializers import ProfileSerializer
# group permission control
from authentication.permissions import isInStaffGroup
# authentication
from authentication.customAuthentication import CustomAuthentication
# importing csv
import csv

# all profiles
class ProfilesListView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])
    
    def get(self, request, format=None):
        try:
            profiles = Students.objects.all().order_by('-id').prefetch_related('phone', 'phone__number_type', 'prefecture', 'grade', 'status', 'payment_method')
            serializer = ProfileSerializer(profiles, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

            
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# profile details
class ProfilesDetailsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    # GET
    def get(self, request, format=None):
        try:
            profile_id = request.GET.get('profile_id')
            profile = Students.objects.get(id=profile_id)
            serializer = ProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # POST
    def post(self, request):
        data = request.data.copy()

        try:
            # sets birthday to None if it is an empty string
            if data['birthday'] == "":
                data['birthday'] = None

            serializer = ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    # PUT
    def put(self, request):
        try:            
            # copies the request data so that it can be modified
            data = request.data.copy()

            # gets the profile to be updated
            profile = Students.objects.get(id=data['profile_id'])

            # sets birthday to None if it is an empty string
            if data['birthday'] == "":
                data['birthday'] = None

            serializer = ProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # DELETE
    def delete(self, request):
        try:
            profile = Students.objects.get(id=request.query_params['profile_id'])
            profile.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

# gets all the choices for the profile create form
class ProfilesChoicesView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request):
        try:
            phone_choices = PhoneChoice.objects.all().order_by('order')
            prefecture_choices = PrefectureChoices.objects.all().order_by('order')
            grade_choices = GradeChoices.objects.all().order_by('order')
            status_choices = StatusChoices.objects.all().order_by('order')
            payment_choices = PaymentChoices.objects.all().order_by('order')

            return Response({
                'phone_choices': phone_choices.values(),
                'prefecture_choices': prefecture_choices.values(),
                'grade_choices': grade_choices.values(),
                'status_choices': status_choices.values(),
                'payment_choices': payment_choices.values(),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# used to import profiles from CSV     
def ProfilesImport(request):
    print('IMPORTING PROFILES')

    profiles_all = Students.objects.all()
    profiles_all.delete()

    phone_all = Phone.objects.all()
    phone_all.delete()

    with open("./static/profile_import.csv") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(row)
            profile = Students()
            profile.last_name_romaji = row[1]
            profile.first_name_romaji = row[2]
            profile.last_name_kanji = row[3]
            profile.first_name_kanji = row[4]
            profile.last_name_katakana = row[18]
            profile.first_name_katakana = row[17]

            if row[5] == '1':
                profile.payment_method = PaymentChoices.objects.get(id=1)
            elif row[5] == '2':
                profile.payment_method = PaymentChoices.objects.get(id=2)

            profile.post_code = row[6]
            profile.address_1 = row[7]
            profile.address_2 = row[8]

            if row[9] != '':
                if row[10] == '0':
                    phone = Phone()
                    phone.number = row[9]
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[10] == '1':
                    phone = Phone()
                    phone.number = row[9]
                    phone.number_type = PhoneChoice.objects.get(id=1)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[10] == '2':
                    phone = Phone()
                    phone.number = row[9]
                    phone.number_type = PhoneChoice.objects.get(id=2)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[10] == '3':
                    phone = Phone()
                    phone.number = row[9]
                    phone.number_type = PhoneChoice.objects.get(id=3)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[10] == '4':
                    phone = Phone()
                    phone.number = row[9]
                    phone.number_type = PhoneChoice.objects.get(id=4)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[10] == '5':
                    phone = Phone()
                    phone.number = row[9]
                    phone.number_type = PhoneChoice.objects.get(id=5)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[10] == '6':
                    phone = Phone()
                    phone.number = row[9]
                    phone.number_type = PhoneChoice.objects.get(id=6)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[10] == '7':
                    phone = Phone()
                    phone.number = row[9]
                    phone.number_type = PhoneChoice.objects.get(id=7)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)

            if row[11] != '':
                if row[12] == '0':
                    phone = Phone()
                    phone.number = row[11]
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[12] == '1':
                    phone = Phone()
                    phone.number = row[11]
                    phone.number_type = PhoneChoice.objects.get(id=1)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[12] == '2':
                    phone = Phone()
                    phone.number = row[11]
                    phone.number_type = PhoneChoice.objects.get(id=2)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[12] == '3':
                    phone = Phone()
                    phone.number = row[11]
                    phone.number_type = PhoneChoice.objects.get(id=3)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[12] == '4':
                    phone = Phone()
                    phone.number = row[11]
                    phone.number_type = PhoneChoice.objects.get(id=4)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[12] == '5':
                    phone = Phone()
                    phone.number = row[11]
                    phone.number_type = PhoneChoice.objects.get(id=5)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[12] == '6':
                    phone = Phone()
                    phone.number = row[11]
                    phone.number_type = PhoneChoice.objects.get(id=6)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)
                if row[12] == '7':
                    phone = Phone()
                    phone.number = row[11]
                    phone.number_type = PhoneChoice.objects.get(id=7)
                    phone.save()
                    profile.save()
                    profile.phone.add(phone)

            if row[13] and row[13] != "NULL":
                profile.birthday = row[13]

            if row[14] == '1':
                profile.grade = GradeChoices.objects.get(id=1)
            elif row[14] == '2':
                profile.grade = GradeChoices.objects.get(id=2)
            elif row[14] == '3':
                profile.grade = GradeChoices.objects.get(id=3)
            elif row[14] == '4':
                profile.grade = GradeChoices.objects.get(id=4)
            elif row[14] == '5':
                profile.grade = GradeChoices.objects.get(id=5)
            elif row[14] == '6':
                profile.grade = GradeChoices.objects.get(id=6)
            elif row[14] == '7':
                profile.grade = GradeChoices.objects.get(id=7)
            elif row[14] == '8':
                profile.grade = GradeChoices.objects.get(id=8)
            elif row[14] == '9':
                profile.grade = GradeChoices.objects.get(id=9)
            elif row[14] == '10':
                profile.grade = GradeChoices.objects.get(id=10)
            elif row[14] == '11':
                profile.grade = GradeChoices.objects.get(id=11)
            elif row[14] == '12':
                profile.grade = GradeChoices.objects.get(id=12)
            elif row[14] == '13':
                profile.grade = GradeChoices.objects.get(id=13)
            elif row[14] == '14':
                profile.grade = GradeChoices.objects.get(id=14)
            elif row[14] == '15':
                profile.grade = GradeChoices.objects.get(id=15)
            elif row[14] == '16':
                profile.grade = GradeChoices.objects.get(id=16)
            elif row[14] == '17':
                profile.grade = GradeChoices.objects.get(id=17)
            elif row[14] == '18':
                profile.grade = GradeChoices.objects.get(id=18)
            elif row[14] == '19':
                profile.grade = GradeChoices.objects.get(id=19)
            elif row[14] == '20':
                profile.grade = GradeChoices.objects.get(id=20)

            if row[15] == '1':
                profile.status = StatusChoices.objects.get(id=1)
            elif row[15] == '2':
                profile.status = StatusChoices.objects.get(id=2)
            elif row[15] == '3':
                profile.status = StatusChoices.objects.get(id=3)
            elif row[15] == '4':
                profile.status = StatusChoices.objects.get(id=4)

            if row[16] == '1':
                profile.prefecture = PrefectureChoices.objects.get(id=1)
            elif row[16] == '2':
                profile.prefecture = PrefectureChoices.objects.get(id=2)

            profile.city = row[19]
            profile.archived = row[20]

            profile.save()

    data = {
        'status': '200 OK',
    }

    return JsonResponse(data)