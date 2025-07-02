from django.http import JsonResponse
from .models import Journal, JournalType
from students.models import Students
from django.contrib.auth.models import User
import csv
from rest_framework.views import APIView
# models
from .models import Journal
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# serializers
from .serializers import GetJournalForProfileSerializer


# get journal entries for a specific profile
class GetJournalForProfileView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, *args, **kwargs):
        profile_id = request.GET.get('profile_id')

        if not profile_id:
            return JsonResponse({'error': 'Profile ID is required'}, status=400)

        try:
            # get journal entries for the student
            journal_entries = Journal.objects.filter(student__id=profile_id).order_by('-date', '-time')

            # serialize the journal entries
            journal_entries_serializer = GetJournalForProfileSerializer(journal_entries, many=True)

            data = {
                'journal_entries': journal_entries_serializer.data
            }
            
            return JsonResponse(data, safe=False)
        
        except Students.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

# used to journal events from CSV     
def JournalImport(request):
    print('')
    print('======= IMPORTING JOURNAL ENTRIES =======')
    print('')

    journal_all = Journal.objects.all()
    journal_all.delete()

    with open("./static/customer_notes.csv") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row

        journal_type = {
            '0' : 3,
            '1' : 4,
            '2' : 5,
            '3' : 6,
            '5' : 7,
            '6' : 8,
            '7' : 9,
            '8' : 10,
            '9' : 11,
            '10': 12,
            '11': 13,
            '12': 14,
            '13': 15,
            '14': 16,
            '15': 17,
        }

        user_translator = {
            '2' : 4,
            '3' : 6,
            '4' : 5,
            '5' : 7,
        }

        for row in reader:
            if row[2] != '4':
                print(row)
                journal         = Journal()
                journal.id      = row[0]
                journal.date    = row[1]
                journal.type    = JournalType.objects.get(id=journal_type[row[2]])
                journal.text    = row[3]
                journal.student = Students.objects.get(id=row[5])
                if row[6] != 'NULL':
                    journal.time    = row[6]
                journal.save()
                if row[7] != 'NULL':
                    journal.instructor.add(User.objects.get(id=user_translator[row[7]]))
                if row[8] != 'NULL':
                    journal.instructor.add(User.objects.get(id=user_translator[row[8]]))
            else:
                print(row)
                journal         = Journal()
                journal.id      = row[0]
                journal.date    = row[1]
                journal.type    = JournalType.objects.get(id=4)
                journal.text    = row[3]
                journal.student = Students.objects.get(id=row[5])
                if row[6] != 'NULL':
                    journal.time    = row[6]
                journal.save()
                if row[7] != 'NULL':
                    journal.instructor.add(User.objects.get(id=user_translator[row[7]]))

                print(row)
                journal         = Journal()
                journal.id      = row[0]
                journal.date    = row[1]
                journal.type    = JournalType.objects.get(id=5)
                journal.text    = row[3]
                journal.student = Students.objects.get(id=row[5])
                if row[6] != 'NULL':
                    journal.time    = row[6]
                journal.save()
                if row[8] != 'NULL':
                    journal.instructor.add(User.objects.get(id=user_translator[row[8]]))

    print('')
    print('======= IMPORT JOURNAL ENTRIES COMPLETE =======')
    print('')

    data = {
        'status': '200 OK',
    }

    return JsonResponse(data)