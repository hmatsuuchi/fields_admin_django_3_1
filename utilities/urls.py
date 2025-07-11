from django.urls import path
# VIEWS
from analytics.views import StudentChurnModelTrain, loop_through_students
from attendance.views import AttendanceImport
from game.views import ImportCardUUID
from journal.views import JournalImport
from schedule.views import EventsImport
from students.views import ProfilesImport, IncrementStudentGrades
from . views import AdjustStudentAttendanceStatus, CleanAttendance, EnumerateAttendance

urlpatterns = [
    # ========== ANALYTICS ==========

    # trains the student churn random forest classifier model
    # path('utilities/student_churn_model_train/', StudentChurnModelTrain.as_view(), name='student_churn_model_train'),

    # loop through list of students
    # path('utilities/loop_through_students/', loop_through_students, name='loop_through_students'),
    




    # ========== ATTENDANCE =========

    # import attendance and attendance records from CSV
    # path('utilities/attendance_import/', AttendanceImport, name='attendance_import'),
    




    # ============= GAME ============

    # import card UUID records from CSV
    # path('utilities/id_import/', ImportCardUUID, name='card_uuid_import'),
    




    # =========== JOURNAL ===========

    # to import journal entries from CSV
    # path('utilities/journal_import/', JournalImport, name='journal_import'),
    




    # =========== SCHEDULE ==========

    # import events from CSV
    # path('utilities/events_import/', EventsImport, name='events_import'),
    




    # =========== STUDENTS ==========

    # import student profiles from CSV
    # path('utilities/profiles_import/', ProfilesImport, name='profiles_import'),

    # increment student grades by one year
    # path('utilities/increment_student_grades/', IncrementStudentGrades, name='increment_student_grades'),





    # ========== UTILITIES ==========

    # adjust student attendance status depending on their attendance records and remove students who have quit from the AtRiskStudents list
    # path('utilities/adjust_student_attendance_status/', AdjustStudentAttendanceStatus, name='adjust_student_attendance_status'),

    # removes attendance that does not have any associated attendance records
    # path('utilities/clean_attendance/', CleanAttendance, name='clean_attendance'),

    # prints attendance for each instructor for each day between current date and cutoff date
    # path('utilities/enumerate_attendance/', EnumerateAttendance, name='enumerate_attendance'),
]