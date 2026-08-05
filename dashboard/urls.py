from django.urls import path
# VIEWS
from . import views

urlpatterns = [
    # Staff Dashboard Endpoints
    path('dashboard/incomplete_attendance_for_instructor/', views.IncompleteAttendanceForInstructorView.as_view(), name='incomplete_attendance_for_instructor'),
    path('dashboard/student_churn/', views.StudentChurnView.as_view(), name='student_churn'),
    path('dashboard/total_active_students/', views.TotalActiveStudentsView.as_view(), name='total_active_students'),
    path('dashboard/total_active_students_historical/', views.TotalActiveStudentsHistoricalView.as_view(), name='total_active_students_historical'),
    path('dashboard/total_active_students_by_grade/', views.TotalActiveStudentsByGrade.as_view(), name='total_active_students_by_grade'),
    path('dashboard/at_risk_students/', views.AtRiskStudentsView.as_view(), name='at_risk_students'),
    path('dashboard/upcoming_birthdays/', views.UpcomingBirthdaysView.as_view(), name='upcoming_birthdays'),
    path('dashboard/at_risk_students/', views.AtRiskStudentsView.as_view(), name='at_risk_students'),

    # Staff Overview Endpoints
    path('dashboard/overview/revenue_by_month/', views.RevenueByMonthView.as_view(), name='revenue_by_month'),
    path('dashboard/overview/revenue_breakdown_by_month/', views.RevenueBreakdownByMonthView.as_view(), name='revenue_breakdown_by_month'),
    path('dashboard/overview/lifetime_data/', views.LifetimeDataView.as_view(), name='lifetime_data'),
    path('dashboard/overview/instructor_data/', views.InstructorDataView.as_view(), name='instructor_data'),
    path('dashboard/overview/attendance_for_all_instructors/', views.AttendanceForAllInstructorsView.as_view(), name='attendance_for_all_instructors'),

    # Customer Dashboard Endpoints
    path('dashboard/invoices_for_customer/', views.InvoicesForCustomerView.as_view(), name='invoices_for_customer'),
    path('dashboard/customer_profile/', views.CustomerProfileDataView.as_view(), name='customer_profile_data')
]