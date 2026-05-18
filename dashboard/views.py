from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, datetime, timedelta
from django.db.models import Count, Q, Min, Max, Prefetch, Sum, F, ExpressionWrapper, IntegerField
from django.utils import timezone
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# models
from user_profiles.models import UserProfilesInstructors
from attendance.models import AttendanceRecord, Attendance
from students.models import Students, GradeChoices
from analytics.models import HighestActiveStudentCount, AtRiskStudents, HighestRevenuePerStudent, HighestLifetimeInDaysPerStudent
from schedule.models import Events
from invoices.models import InvoiceItem
# serializers
from dashboard.serializers import AtRiskStudentSerializer
from dashboard.serializers import UpcomingBirthdayStudentSerializer

# get all incomplete recent attendance records for an instructor
class IncompleteAttendanceForInstructorView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get the current user
            current_user = request.user

            # get all records for the instructor for the past month
            past_month = AttendanceRecord.objects.filter(attendance_reverse_relationship__instructor=current_user, attendance_reverse_relationship__date__gte=datetime.now() - timedelta(days=30), attendance_reverse_relationship__date__lte=datetime.now())

            # group the records by date
            past_month_by_date = past_month.order_by('-attendance_reverse_relationship__date').values('attendance_reverse_relationship__date')

            # annotate records with attendance status counts
            past_month_by_date_annotated = past_month_by_date.annotate(record_count_all=Count('id'), record_count_incomplete=Count('id', filter=Q(status=2)), record_count_present=Count('id', filter=Q(status=3)), record_count_absent=Count('id', filter=Q(status=4)))

            # get the instructor's working days preference
            instructor_profile = UserProfilesInstructors.objects.get(user=current_user)
            working_days = instructor_profile.pref_dashboard_working_days

            data = {
                'past_month_by_date_annotated': past_month_by_date_annotated,
                'pref_dashboard_working_days': working_days,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
# get student churn data
class StudentChurnView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            # get students with two or more present attendance records
            students_with_attendance = (
                Students.objects
                .annotate(
                    present_count = Count('attendancerecord', filter=Q(attendancerecord__status=3)),
                    earliest_present = Min('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                    latest_present = Max('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                )
                .filter(present_count__gte=2)
                .order_by('earliest_present')
            )

            # create a list of years, months, starting students, ending students
            churn_data = []
            today = date.today()
            start_date = today - timedelta(days=365 * 2)  # 2 years ago
            current_date = start_date

            # iterate through each month from start_date to today
            while current_date <= today:
                # get the start of the month
                month_start = current_date.replace(day=1)
                # get the end of the month
                next_month = (month_start + timedelta(days=31)).replace(day=1)
                month_end = next_month - timedelta(days=1)

                # Students who started in this month
                starting_students = [
                    student for student in students_with_attendance
                    if month_start <= student.earliest_present <= month_end
                ]

                # Students who ended in this month and latest_present is more than 4 weeks ago
                ending_students = [
                    student for student in students_with_attendance
                    if month_start <= student.latest_present <= month_end and (today - student.latest_present).days > 28
                ]

                churn_data.append({
                    'year': month_start.year,
                    'month': month_start.month,
                    'starting_students_count': len(starting_students),
                    'ending_students_count': len(ending_students),
                    'starting_students_list': [
                        {
                            'id': student.id,
                            'last_name_romaji': student.last_name_romaji,
                            'first_name_romaji': student.first_name_romaji,
                            'start_date': student.earliest_present,
                        }
                        for student in starting_students
                    ],
                    'ending_students_list': [
                        {
                            'id': student.id,
                            'last_name_romaji': student.last_name_romaji,
                            'first_name_romaji': student.first_name_romaji,
                            'end_date': student.latest_present,
                        }
                        for student in ending_students
                    ],
                })

                # move to the next month
                current_date = next_month

            return Response(churn_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# get total active students data
class TotalActiveStudentsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            cutoff_date = date.today() - timedelta(days=28)

            # active students are those with at least two present (status=3) attendance records, and at least one of those records is within the last 28 days
            active_students = (
                Students.objects
                .annotate(
                    attendance_count=Count('attendancerecord', filter=Q(attendancerecord__status=3)),
                    most_recent=Max('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3))
                )
                .filter(
                    attendance_count__gte=2,
                    most_recent__gte=cutoff_date
                )
                .distinct()
            )

            # gets the count of active students
            active_students_count = active_students.count()

            # gets the highest active student count
            highest_active_student_count = HighestActiveStudentCount.objects.order_by('-active_student_count').first()

            if not highest_active_student_count:
                # if no records exist, create a new record with the current count
                highest_active_student_count = HighestActiveStudentCount.objects.create(
                    active_student_count=active_students_count
                )
            elif highest_active_student_count.active_student_count < active_students_count:
                # if the current count is higher than the stored count, create a new record with the current count
                highest_active_student_count = HighestActiveStudentCount.objects.create(
                    active_student_count=active_students_count
                )


            data = {
                'total_active_students_count': active_students_count,
                'highest_active_student_count': {
                    'count': highest_active_student_count.active_student_count,
                    'date': highest_active_student_count.date_time_created,
                },
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get historical data of total active students
class TotalActiveStudentsHistoricalView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # get students with two or more present attendance records
            students_with_attendance = (
                Students.objects
                .annotate(
                    present_count = Count('attendancerecord', filter=Q(attendancerecord__status=3)),
                    earliest_present = Min('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                    latest_present = Max('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                )
                .filter(present_count__gte=2)
            )

            # create a list of historical data
            historical_data = []
            # iterative parameters to generate historical data
            today = date.today()
            start_date = today - timedelta(days=365 * 2)  # 2 years ago
            current_date = start_date

            # iterate through each month from start_date to today
            while current_date <= today:
                # get the start of the current month
                current_month_start = current_date.replace(day=1)

                # get the start and end of the next month
                next_month_start = (current_month_start + timedelta(days=31)).replace(day=1)

                # count active students for the month
                active_students_count = sum(
                    1 for student in students_with_attendance
                    if student.earliest_present < next_month_start and student.latest_present >= current_month_start
                )

                historical_data.append({
                    'year': current_month_start.year,
                    'month': current_month_start.month,
                    'active_students_count': active_students_count,
                })

                # move to the next month
                current_date = next_month_start

            return Response(historical_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get historical data of total active students by grade
class TotalActiveStudentsByGrade(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):
        try:
            # 1 - fetch data from DB
            # two year time window to prefetch data
            today = date.today()
            start_date = today - timedelta(days=365 * 2)

            # get students with two or more present attendance records
            students_with_attendance = (
                Students.objects
                .annotate(
                    present_count = Count('attendancerecord', filter=Q(attendancerecord__status=3)),
                    earliest_present = Min('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                    latest_present = Max('attendancerecord__attendance_reverse_relationship__date', filter=Q(attendancerecord__status=3)),
                )
                .prefetch_related(
                    Prefetch(
                        'attendancerecord_set',
                        queryset=AttendanceRecord.objects.filter(
                            status_id=3,  # present only — skip non-present records entirely
                            attendance_reverse_relationship__date__gte=start_date,
                        ).distinct().prefetch_related(
                            Prefetch(
                                'attendance_reverse_relationship',
                                queryset=Attendance.objects.filter(date__gte=start_date)
                            )
                        )
                    )
                )
                .filter(present_count__gte=2)
            )

            # 2 - Single pass: build (student_id, year, month) -> grade_id lookup
            # This replaces get_latest_grade_in_month() entirely
            student_month_grade = {}  # key: (student_id, year, month), value: grade_id

            for student in students_with_attendance:
                for record in student.attendancerecord_set.all():
                    for attendance in record.attendance_reverse_relationship.all():
                        key = (student.id, attendance.date.year, attendance.date.month)
                        existing = student_month_grade.get(key)
                        if existing is None or attendance.date > existing[0]:
                            student_month_grade[key] = (attendance.date, record.grade_id)

            # 3 - Generate historical data with a single pass through months
            grade_choices = GradeChoices.objects.all()
            grade_map = {grade.id: grade.name for grade in grade_choices}

            historical_data = []
            current_date = start_date

            # iterate through each month from start_date to today
            while current_date <= today:
                # get the start of the current month
                current_month_start = current_date.replace(day=1)

                # get the start and end of the next month
                next_month_start = (current_month_start + timedelta(days=31)).replace(day=1)
                next_month_end = next_month_start - timedelta(days=1)

                # count active students for the month
                active_students_this_month = [
                    s for s in students_with_attendance
                    if s.earliest_present < next_month_start and s.latest_present >= current_month_start
                ]
                total_active_students_count = len(active_students_this_month)  # free — no second pass

                # count active students by grade for the month
                counts_by_grade = {name: 0 for name in grade_map.values()}
                for student in active_students_this_month:
                    key = (student.id, current_month_start.year, current_month_start.month)
                    entry = student_month_grade.get(key)
                    if entry:
                        grade_name = grade_map.get(entry[1])
                        if grade_name:
                            counts_by_grade[grade_name] += 1

                historical_data.append({
                    'year': current_month_start.year,
                    'month': current_month_start.month,
                    'total': total_active_students_count,
                    **counts_by_grade
                })

                # move to the next month
                current_date = next_month_start

            return Response(historical_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get list of students at risk of churn
class AtRiskStudentsView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:

            # get at risk student list
            at_risk_students = AtRiskStudents.objects.all().order_by('-date_time_created')

            # serialize student list
            serializer = AtRiskStudentSerializer(at_risk_students, many=True)

            data = {
                'at_risk_students': serializer.data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# get list of students with upcoming birthdays
class UpcomingBirthdaysView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            start_date          = datetime.now() # today
            day_of_week_today   = start_date.weekday() # day of the week (0=Monday, 6=Sunday)

            # date_offset         = 0
            # start_date          = datetime.now() + timedelta(days=date_offset)
            # day_of_week_today   = start_date.weekday()

            # create a list of (month, day) tuples for the next 7 days
            date_list = [
                (d.month, d.day)
                for d in (start_date + timedelta(days=i) for i in range(7))
            ]

            # create a Q object to hold the OR conditions
            q_objects = Q()
            for month, day in date_list:
                q_objects |= Q(birthday__month=month, birthday__day=day)

            # get all active students
            active_students = Students.objects.filter(status=2)

            # filter by active lessons on current day of the week
            students_with_lessons_today = active_students.filter(events__day_of_week=day_of_week_today, events__archived=False).distinct()

            # students with birthday data
            students_with_birthday_data = students_with_lessons_today.filter(
                birthday__isnull=False
            )
            
            # students with birthdays within the next 7 days
            students_with_upcoming_birthdays = students_with_birthday_data.filter(q_objects).annotate(earliest_event_start_time=Min('events__start_time')).order_by('earliest_event_start_time')

            # get related objects to reduce queries
            students_with_upcoming_birthdays = students_with_upcoming_birthdays.prefetch_related(Prefetch('events_set', queryset=Events.objects.filter(day_of_week=day_of_week_today, archived=False)))

            # serialize data
            serializer = UpcomingBirthdayStudentSerializer(students_with_upcoming_birthdays, many=True)

            birthday_data = serializer.data

            return Response(birthday_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# get revenue by month
class RevenueByMonthView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            # paid revenue by month
            invoice_items_paid = InvoiceItem.objects.filter(
                invoice__paid_date__isnull=False
                ).values(
                'invoice__year',
                'invoice__month',
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('invoice__year', 'invoice__month')

            # unpaid revenue by month
            invoice_items_unpaid = InvoiceItem.objects.filter(
                invoice__paid_date__isnull=True
                ).values(
                'invoice__year',
                'invoice__month',
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('invoice__year', 'invoice__month')

            # create a list of years, months, total revenue, unpaid revenue
            today = timezone.localdate() # today
            working_year = today.year - 2 # set year to 2 years ago
            working_month = today.month 

            monthly_revenue_data = [] # list for response data

            # adjust working year and month to have a starting point of no sooner than 2026/01
            if (working_year < 2026):
                working_year = 2026
                working_month = 1

            while (working_year, working_month) <= (today.year, today.month):
                # get paid revenue data for year/month
                paid_revenue_data = next((item for item in invoice_items_paid if item['invoice__year'] == working_year and item['invoice__month'] == working_month), None)
                paid_revenue = paid_revenue_data['total_revenue'] if paid_revenue_data else 0

                # get unpaid revenue data for year/month
                unpaid_revenue_data = next((item for item in invoice_items_unpaid if item['invoice__year'] == working_year and item['invoice__month'] == working_month), None)
                unpaid_revenue = unpaid_revenue_data['total_revenue'] if unpaid_revenue_data else 0

                month_data = {
                    'year': working_year,
                    'month': working_month,
                    'paid_revenue': paid_revenue,
                    'unpaid_revenue': unpaid_revenue,
                }

                monthly_revenue_data.append(month_data)

                # increments to next year/month
                if working_month == 12:
                    working_month = 1
                    working_year += 1
                else:
                    working_month += 1

            data = {
                'monthly_revenue_data': monthly_revenue_data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# get revenue by month
class RevenueBreakdownByMonthView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            # lesson revenue by month
            invoice_items_lessons = InvoiceItem.objects.filter(
                service_type__revenue_type__id=1, # lesson revenue type
                ).values(
                'invoice__year',
                'invoice__month',
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('invoice__year', 'invoice__month')

            # entrance fee revenue by month
            invoice_items_entrance_fee = InvoiceItem.objects.filter(
                service_type__revenue_type__id=2, # entrance fee revenue type
                ).values(
                'invoice__year',
                'invoice__month',
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('invoice__year', 'invoice__month')

            # discounts given by month
            invoice_items_discounts = InvoiceItem.objects.filter(
                service_type__revenue_type__id=3, # discounts revenue type
                ).values(
                'invoice__year',
                'invoice__month',
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('invoice__year', 'invoice__month')

            # teaching materials revenue by month
            invoice_items_teaching_materials = InvoiceItem.objects.filter(
                service_type__revenue_type__id=4, # teaching materials revenue type
                ).values(
                'invoice__year',
                'invoice__month',
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('invoice__year', 'invoice__month')

            # refunds given by month
            invoice_items_refunds = InvoiceItem.objects.filter(
                service_type__revenue_type__id=5, # refunds revenue type
                ).values(
                'invoice__year',
                'invoice__month',
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('invoice__year', 'invoice__month')

            # create a list of years, months, total revenue, unpaid revenue
            today = timezone.localdate() # today
            working_year = today.year - 2 # set year to 2 years ago
            working_month = today.month 

            monthly_revenue_data = [] # list for response data

            # adjust working year and month to have a starting point of no sooner than 2026/01
            if (working_year < 2026):
                working_year = 2026
                working_month = 1

            while (working_year, working_month) <= (today.year, today.month):
                # get lesson revenue data for year/month
                lesson_revenue_data = next((item for item in invoice_items_lessons if item['invoice__year'] == working_year and item['invoice__month'] == working_month), None)
                lesson_revenue = lesson_revenue_data['total_revenue'] if lesson_revenue_data else 0

                # get entrance fee revenue data for year/month
                entrance_fee_revenue_data = next((item for item in invoice_items_entrance_fee if item['invoice__year'] == working_year and item['invoice__month'] == working_month), None)
                entrance_fee_revenue = entrance_fee_revenue_data['total_revenue'] if entrance_fee_revenue_data else 0

                # get discounts given data for year/month
                discounts_given_data = next((item for item in invoice_items_discounts if item['invoice__year'] == working_year and item['invoice__month'] == working_month), None)
                discounts_given = discounts_given_data['total_revenue'] if discounts_given_data else 0

                # get teaching materials revenue data for year/month
                teaching_materials_revenue_data = next((item for item in invoice_items_teaching_materials if item['invoice__year'] == working_year and item['invoice__month'] == working_month), None)
                teaching_materials_revenue = teaching_materials_revenue_data['total_revenue'] if teaching_materials_revenue_data else 0

                # get refunds given data for year/month
                refunds_given_data = next((item for item in invoice_items_refunds if item['invoice__year'] == working_year and item['invoice__month'] == working_month), None)
                refunds_given = refunds_given_data['total_revenue'] if refunds_given_data else 0

                month_data = {
                    'year': working_year,
                    'month': working_month,
                    'lesson_revenue': lesson_revenue,
                    'entrance_fee_revenue': entrance_fee_revenue,
                    'discounts_given': discounts_given,
                    'teaching_materials_revenue': teaching_materials_revenue,
                    'refunds_given': refunds_given,
                }

                monthly_revenue_data.append(month_data)

                # increments to next year/month
                if working_month == 12:
                    working_month = 1
                    working_year += 1
                else:
                    working_month += 1

            data = {
                'monthly_revenue_data': monthly_revenue_data,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# calculate average lifetime revenue per student
class LifetimeDataView(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, format=None):        
        try:
            # 1 - calculate total revenue per student
            revenue_per_student = InvoiceItem.objects.filter(
                invoice__paid_date__isnull=False
            ).values(
                'invoice__student__id'
            ).annotate(
                total_revenue=Sum(
                    ExpressionWrapper(F('quantity') * F('rate'), output_field=IntegerField())
                )
            ).order_by('total_revenue')

            # calculate mean and median lifetime revenue per student
            mean_revenue = revenue_per_student.aggregate(mean_revenue=Sum('total_revenue') / Count('invoice__student__id'))['mean_revenue']
            median_revenue = revenue_per_student[len(revenue_per_student) // 2]['total_revenue'] if revenue_per_student else 0

            # get the highest mean and median revenue per student record
            highest_mean_revenue = HighestRevenuePerStudent.objects.filter(value_type='mean').order_by('-revenue_per_student').first()
            highest_median_revenue = HighestRevenuePerStudent.objects.filter(value_type='median').order_by('-revenue_per_student').first()

            # if no record exists or current mean/median revenue is higher than the stored value, create a new record
            if not highest_mean_revenue or mean_revenue > highest_mean_revenue.revenue_per_student:
                new_record_mean = HighestRevenuePerStudent.objects.create(
                    revenue_per_student=mean_revenue,
                    value_type='mean'
                )

                highest_mean_revenue = new_record_mean
            
            if not highest_median_revenue or median_revenue > highest_median_revenue.revenue_per_student:
                new_record_median = HighestRevenuePerStudent.objects.create(
                    revenue_per_student=median_revenue,
                    value_type='median'
                )

                highest_median_revenue = new_record_median
            
            # 2 - calculate average lifetime per student in days
            lifetime_data = AttendanceRecord.objects.filter(
                status=3
            ).values(
                'student__id'
            ).annotate(
                present_count=Count('id'),
            ).filter(
                present_count__gte=2
            ).annotate(
                first_attendance=Min('attendance_reverse_relationship__date'),
                last_attendance=Max('attendance_reverse_relationship__date'),
            )

            lifetimes = [
                (row['last_attendance'] - row['first_attendance']).days
                for row in lifetime_data
                if row['first_attendance'] and row['last_attendance']
            ]

            mean_lifetime_days = sum(lifetimes) // len(lifetimes) if lifetimes else 0
            median_lifetime_days = sorted(lifetimes)[len(lifetimes) // 2] if lifetimes else 0

            # get the highest mean and median lifetime in days per student record
            highest_mean_lifetime = HighestLifetimeInDaysPerStudent.objects.filter(value_type='mean').order_by('-lifetime_in_days_per_student').first()
            highest_median_lifetime = HighestLifetimeInDaysPerStudent.objects.filter(value_type='median').order_by('-lifetime_in_days_per_student').first()

            # if no record exists or current mean/median lifetime is higher than the stored value, create a new record
            if not highest_mean_lifetime or mean_lifetime_days > highest_mean_lifetime.lifetime_in_days_per_student:
                new_record_mean_lifetime = HighestLifetimeInDaysPerStudent.objects.create(
                    lifetime_in_days_per_student=mean_lifetime_days,
                    value_type='mean'
                )

                highest_mean_lifetime = new_record_mean_lifetime

            if not highest_median_lifetime or median_lifetime_days > highest_median_lifetime.lifetime_in_days_per_student:
                new_record_median_lifetime = HighestLifetimeInDaysPerStudent.objects.create(
                    lifetime_in_days_per_student=median_lifetime_days,
                    value_type='median'
                )

                highest_median_lifetime = new_record_median_lifetime
            

            data = {
                'mean_lifetime_revenue': mean_revenue,
                'highest_mean_lifetime_revenue': highest_mean_revenue.revenue_per_student if highest_mean_revenue else None,
                'highest_mean_lifetime_revenue_date': highest_mean_revenue.date_time_created if highest_mean_revenue else None,
                'median_lifetime_revenue': median_revenue,
                'highest_median_lifetime_revenue': highest_median_revenue.revenue_per_student if highest_median_revenue else None,
                'highest_median_lifetime_revenue_date': highest_median_revenue.date_time_created if highest_median_revenue else None,
                'mean_lifetime_in_days': mean_lifetime_days,
                'highest_mean_lifetime_in_days': highest_mean_lifetime.lifetime_in_days_per_student if highest_mean_lifetime else None,
                'highest_mean_lifetime_in_days_date': highest_mean_lifetime.date_time_created if highest_mean_lifetime else None,
                'median_lifetime_in_days': median_lifetime_days,
                'highest_median_lifetime_in_days': highest_median_lifetime.lifetime_in_days_per_student if highest_median_lifetime else None,
                'highest_median_lifetime_in_days_date': highest_median_lifetime.date_time_created if highest_median_lifetime else None,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)