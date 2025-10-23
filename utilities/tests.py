from django.test import TestCase

# ==================================
# ======= UTILITY VIEW TESTS =======
# ==================================

# ============= ACCESS PERMISSIONS =============

# student churn model train view is NOT ACCESSIBLE to anyone
class StudentChurnModelTrainAccessPermissionsTests(TestCase):
    def test_student_churn_model_train_view_not_accessible(self):
        response = self.client.get('/utilities/student_churn_model_train/')
        self.assertEqual(response.status_code, 404)

# loop through list of students view is NOT ACCESSIBLE to anyone
class LoopThroughStudentsAccessPermissionsTests(TestCase):
    def test_loop_through_students_view_not_accessible(self):
        response = self.client.get('/utilities/loop_through_students/')
        self.assertEqual(response.status_code, 404)

# attendance import view is NOT ACCESSIBLE to anyone
class AttendanceImportAccessPermissionsTests(TestCase):
    def test_attendance_import_view_not_accessible(self):
        response = self.client.get('/utilities/attendance_import/')
        self.assertEqual(response.status_code, 404)

# card UUID import view is NOT ACCESSIBLE to anyone
class ImportCardUUIDAccessPermissionsTests(TestCase):
    def test_import_card_uuid_view_not_accessible(self):
        response = self.client.get('/utilities/id_import/')
        self.assertEqual(response.status_code, 404)

# journal import view is NOT ACCESSIBLE to anyone
class JournalImportAccessPermissionsTests(TestCase):
    def test_journal_import_view_not_accessible(self):
        response = self.client.get('/utilities/journal_import/')
        self.assertEqual(response.status_code, 404)

# events import view is NOT ACCESSIBLE to anyone
class EventsImportAccessPermissionsTests(TestCase):
    def test_events_import_view_not_accessible(self):
        response = self.client.get('/utilities/events_import/')
        self.assertEqual(response.status_code, 404)

# profiles import view is NOT ACCESSIBLE to anyone
class ProfilesImportAccessPermissionsTests(TestCase):
    def test_profiles_import_view_not_accessible(self):
        response = self.client.get('/utilities/profiles_import/')
        self.assertEqual(response.status_code, 404)

# increment student grades view is NOT ACCESSIBLE to anyone
class IncrementStudentGradesAccessPermissionsTests(TestCase):
    def test_increment_student_grades_view_not_accessible(self):
        response = self.client.get('/utilities/increment_student_grades/')
        self.assertEqual(response.status_code, 404)

# adjust attendance status view is NOT ACCESSIBLE to anyone
class AdjustAttendanceStatusAccessPermissionsTests(TestCase):
    def test_adjust_attendance_status_view_not_accessible(self):
        response = self.client.get('/utilities/adjust_student_attendance_status/')
        self.assertEqual(response.status_code, 404)

# clean attendance view is NOT ACCESSIBLE to anyone
class CleanAttendanceAccessPermissionsTests(TestCase):
    def test_clean_attendance_view_not_accessible(self):
        response = self.client.get('/utilities/clean_attendance/')
        self.assertEqual(response.status_code, 404)

# print attendance for each instructor view is NOT ACCESSIBLE to anyone
class PrintAttendanceForInstructorsAccessPermissionsTests(TestCase):
    def test_print_attendance_for_instructors_view_not_accessible(self):
        response = self.client.get('/utilities/enumerate_attendance/')
        self.assertEqual(response.status_code, 404)