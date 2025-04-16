from django.contrib import admin
from django.urls import path, include
from .views import LoggedInUserDataView
# custom simple jwt authentication
from authentication.customTokenObtainPair import CustomTokenObtainPairView, CustomTokenRefreshView
# URLS
import authentication.urls as AuthenticationUrls
import students.urls as StudentsUrls
import schedule.urls as ScheduleUrls
import attendance.urls as AttendanceUrls
import journal.urls as JournalUrls
import dashboard.urls as DashboardUrls

urlpatterns = [
    path('admin/', admin.site.urls),

    # simple jwt authentication
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(AuthenticationUrls)),

    # student profiles
    path('api/students/', include(StudentsUrls)),

    # schedule
    path('api/schedule/', include(ScheduleUrls)),

    # attendance
    path('api/attendance/', include(AttendanceUrls)),

    # journal
    path('api/journal/', include(JournalUrls)),

    # logged in user data
    path('api/logged_in_user_data/', LoggedInUserDataView.as_view(), name='logged_in_user_data'),

    # dashboard
    path('api/dashboard/', include(DashboardUrls)),
]
