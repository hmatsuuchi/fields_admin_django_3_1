from datetime import date, timedelta
from django.db.models import Max, Q, Count
from django.http import JsonResponse
# models
from students.models import Students, StatusChoices
from analytics.models import AtRiskStudents
from attendance.models import Attendance

# adjust student attendance status depending on their attendance records
# also removes students who have quite from the AtRiskStudents list
def AdjustStudentAttendanceStatus(request):
    # sets the cutoff date for students to be considered present
    cutoff_date = date.today() - timedelta(days=28)

    # get all students and annotate students with their most recent present attendance record
    students = Students.objects.annotate(
        most_recent_present=Max(
            'attendancerecord__attendance_reverse_relationship__date',
            filter=Q(attendancerecord__status=3)
        ),
        present_attendance_count=Count('attendancerecord', filter=Q(attendancerecord__status=3))
    )

    enrolled_students = students.filter(
        most_recent_present__gte=cutoff_date,
        present_attendance_count__gte=2,
    )

    quit_students = students.filter(
        Q(most_recent_present__lt=cutoff_date) | Q(most_recent_present__isnull=True) | Q(present_attendance_count__lt=2)
    )

    print( f"========== ENROLLED STUDENTS [{len(enrolled_students)}] ==========" )
    for student in enrolled_students:
        if student.status.id != 2:  # if student is enrolled
            print(f"{student.last_name_romaji}, {student.first_name_romaji} [{student.status.id} -> 2 (enrolled)]")
            student.status = StatusChoices.objects.get(id=2)  # set status to enrolled
            student.save()

    print( f"============ QUIT STUDENTS [{len(quit_students)}] ============" )
    for student in quit_students:
        if student.status.id not in [1, 3, 4]:
            print(f"{student.last_name_romaji}, {student.first_name_romaji} [{student.status.id} -> 3 (short-absence)]")
            student.status = StatusChoices.objects.get(id=3)
            student.save()

    # get at risk students list
    at_risk_students = AtRiskStudents.objects.all()

    # remove students who have quit from the AtRiskStudents list
    for student in quit_students:
        if at_risk_students.filter(student=student).exists():
            print(f"Removing {student.last_name_romaji}, {student.first_name_romaji} from AtRiskStudents")
            at_risk_students.filter(student=student).delete()

    return JsonResponse({'status': '200 OK'})

# removes attendance that does not have any associated attendance records
def CleanAttendance(request):
    # get all attendance and annotate with the count of associated attendance records
    attendance = Attendance.objects.annotate(
        attendance_record_count=Count('attendance_records')
    ).filter(attendance_record_count=0)

    for x in attendance:
        print(x.linked_class)
        print(x.instructor)
        print(x.attendance_records.all())
        print(x.date)
        print(x.start_time)
        print("=" * 50)
        x.delete()

    return JsonResponse({'status': '200 OK'})

# prints attendance for each instructor for each day between current date and cutoff date
def EnumerateAttendance(request):
    # set cutoff date
    cutoff_date = date.today() - timedelta(days=28)

    # get all attendance since the cutoff date
    attendance = Attendance.objects.filter(date__gte=cutoff_date).order_by('date', 'instructor')

    # iterate through dates and print attendance details for each instructor
    current_date = cutoff_date
    while current_date <= date.today():
        print("")
        print( f"================ {current_date} ================" )
        print("")

        # get attendance for the current date
        attendance_for_date = attendance.filter(date=current_date)

        # attendance for Hiroki (id=4)
        attendance_hiroki = attendance_for_date.filter(instructor__id=4)

        # attendance for David (id=5)
        attendance_david = attendance_for_date.filter(instructor__id=5)

        # attendance for Lauren (id=8)
        attendance_lauren = attendance_for_date.filter(instructor__id=8)

        # attendance for Motoyo (id=6)
        attendance_motoyo = attendance_for_date.filter(instructor__id=6)

        # print attendance details
        for x in attendance_hiroki:
            print(x.linked_class)
        print("-" * 30)

        for x in attendance_david:
            print(x.linked_class)
        print("-" * 30)

        for x in attendance_lauren:
            print(x.linked_class)
        print("-" * 30)

        for x in attendance_motoyo:
            print(x.linked_class)
        print("-" * 30)

        # increment current date
        current_date += timedelta(days=1)

    return JsonResponse({'status': '200 OK'})