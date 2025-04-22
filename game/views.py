
from django.http import JsonResponse
# models
from .models import CardUUID
from students.models import Students
# importing csv
import csv

# used to import attendance records from CSV
def ImportCardUUID(request):
    print('')
    print('======= IMPORTING CARD UUIDs =======')
    print('')

    # delete all previous records
    CardUUID.objects.all().delete()

    # import card UUID CSV
    with open('./static/game_cardindex.csv') as file:
        card_index_reader = csv.reader(file)
        next(card_index_reader)

        for row in card_index_reader:
            CardUUID.objects.create(
                card_uuid=row[1],
                linked_student=Students.objects.get(id=row[2]),
            )

    print('======= IMPORT COMPLETE =======')

    return JsonResponse({'status': '200 OK'})