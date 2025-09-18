from datetime import date, timedelta
from django.db.models import Count, Max, Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
# authentication
from authentication.customAuthentication import CustomAuthentication
# group permission control
from authentication.permissions import isInStaffGroup
# models
from attendance.models import AttendanceRecord
from students.models import Students
from analytics.models import AtRiskStudents, StudentChurnModelTrainingHistory
# machine learning imports
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score
import joblib

# ========================== FUNCTIONS ==========================
def clean_normalize_data(student):
    # ============ ATTENDANCE / IS ACTIVE ============
    # converts attendance records to binary data and normalizes the length of list
    # students without present attendance in the last 28 days are considdered as having quit
    cutoff_date = date.today() - timedelta(days=28)

    # determine if the student has been present in the last 28 days
    currently_active = student.most_recent_present > cutoff_date

    # fetch all attendance records for the student ordered by attendance date
    attendance_records = (
        AttendanceRecord.objects
        .filter(student=student)
        .order_by('attendance_reverse_relationship__date')
        .select_related('status')
        .prefetch_related('attendance_reverse_relationship')
    )

    # normalizes the length of attendance records to a fixed length
    normalized_attendance_record_length = 300

    # creates a list of attendance data for the student 0 = absent, 1 = present
    attendance_data = []
    for record in attendance_records:
        if record.status.id == 3:
            attendance_data.append(1)
        else:
            attendance_data.append(0)

    # makes length of attendance record array equal to normalized_attendance_record_length
    if len(attendance_data) < normalized_attendance_record_length:
        padding = [0] * (normalized_attendance_record_length - len(attendance_data))
        attendance_data = padding + attendance_data

    # ============ AGE AT TIME OF MOST RECENT PRESENT ATTENDANCE RECORD ============
    age_at_most_recent_present = 999

    if student.birthday:
        # calculates age in years at the time of most recent present attendance record
        birthday = student.birthday
        present_date = student.most_recent_present
        years = present_date.year - birthday.year
        # Adjust if the birthday hasn't occurred yet this year
        if (present_date.month, present_date.day) < (birthday.month, birthday.day):
            years -= 1
        age_at_most_recent_present = years

    # print(f"{student.first_name_romaji}, {student.last_name_romaji}")
    # print(student.birthday)
    # print(f"Age at Most Recent Present: {age_at_most_recent_present}")
    # print(f"Attendance Record Length: {len(attendance_data)}")
    # print("-" * 50)

    return {
            'attendance': attendance_data,
            'age_at_most_recent_present': age_at_most_recent_present,
            'currently_active': 1 if currently_active else 0,
        }

# LOOP THROUGH STUDENTS AND PRINT DATA (FOR TESTING PURPOSES)
def loop_through_students(request):
    # cutoff date of 28 days ago
    cutoff_date = date.today() - timedelta(days=28)

    # get students
    students = Students.objects.annotate(
        attendance_record_count=Count('attendancerecord',
        filter=Q(attendancerecord__status=3) | Q(attendancerecord__status=4),
        ),
        most_recent_present=Max(
            'attendancerecord__attendance_reverse_relationship__date',
            filter=Q(attendancerecord__status=3)
        ),
    ).filter(attendance_record_count__gte=2)

    # get students without birthday data
    students_without_birthday = students.filter(birthday__isnull=True)

    # get students with status=3 (present) attendance in the last 28 days
    students_with_recent_attendance = students.filter(most_recent_present__gte=cutoff_date)

    for student in students:
        age_at_most_recent_present = None
        if student.birthday:
            # calculates age in years at the time of most recent present attendance record
            birthday = student.birthday
            present_date = student.most_recent_present
            years = present_date.year - birthday.year
            # Adjust if the birthday hasn't occurred yet this year
            if (present_date.month, present_date.day) < (birthday.month, birthday.day):
                years -= 1
            age_at_most_recent_present = years

            # creates a list of binary values for student age at most recent present attendance
            age_binary = [0] * 22 # 0 - 20 and over 20
            if age_at_most_recent_present is not None:
                if age_at_most_recent_present < 20:
                    age_binary[age_at_most_recent_present] = 1
                else:
                    age_binary[20] = 1

        print(f"{student.first_name_romaji} {student.last_name_romaji}")
        print(student.birthday)
        print(age_at_most_recent_present)
        print(age_binary)
        print("-" * 50)

    print("")
    print("=" * 50)
    print(f"Student Count: {students.count()}")
    print(f"Students Without Birthday Data Count: {students_without_birthday.count()}")
    print(f"Students Recent Attendance Count: {students_with_recent_attendance.count()}")
    print("=" * 50)
    print("")

    return JsonResponse({'status': '200 OK'})

# TRAIN RANDOM FOREST CLASSIFIER ON STUDENT ATTENDANCE DATA (STUDENT CHURN)
class StudentChurnModelTrain(APIView): 
    def get(self, request, format=None):
        try:
            # ================ CLEANING DATA FOR ML ANALYSIS ================
            # data for ML analysis
            cleaned_data = []

            # Annotate each student with their most recent status=3 (present) attendance date
            students = Students.objects.annotate(
                attendance_count = Count('attendancerecord'),
                most_recent_present = Max(
                    'attendancerecord__attendance_reverse_relationship__date',
                    filter=Q(attendancerecord__status = 3),                )
            ).filter(attendance_count__gte=2)

            for student in students:
                cleaned_data.append(clean_normalize_data(student))



            # ============================ NUMPY ============================
            # extract features (X) and labels (y)
            X = [data['attendance'] + [data['age_at_most_recent_present']] for data in cleaned_data]
            y = [data['currently_active'] for data in cleaned_data]

            # convert to numpy arrays
            X = np.array(X)
            y = np.array(y)




            # =================== SCIKIT-LEARN - TRAINING ===================
            # Split into train/test sets (optional but recommended)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Create and train the classifier
            clf = RandomForestClassifier(n_estimators=500, random_state=42)
            clf.fit(X_train, y_train)

            # Predict on test set
            y_pred = clf.predict(X_test)

            # Evaluate accuracy
            from sklearn.metrics import accuracy_score

            # Save model training history
            training_history = StudentChurnModelTrainingHistory(
                model_name='Second Generation',
                model_accuracy=accuracy_score(y_test, y_pred),
                model_f1_score=f1_score(y_test, y_pred, average='weighted'),
                model_precision=precision_score(y_test, y_pred, average='weighted'),
                model_recall=recall_score(y_test, y_pred, average='weighted'),
            )
            training_history.save()


            # ================== SCIKIT-LEARN - SAVE MODEL ==================
            # Build the path to the sibling ml_models directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ml_models_dir = os.path.join(base_dir, 'analytics/ml_models')
            os.makedirs(ml_models_dir, exist_ok=True)  # Ensure directory exists

            model_filename = os.path.join(ml_models_dir, 'student_churn_model.pkl')
            joblib.dump(clf, model_filename)



            data = {
                'status': 'HTTP_200_OK',
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# PREDICT STUDENT CHURN USING RANDOM FOREST CLASSIFIER FOR ATTENDANCE RECORD
class StudentChurnModelPredictForAttendanceRecord(APIView):
    authentication_classes = ([CustomAuthentication])
    permission_classes = ([isInStaffGroup])

    def get(self, request, attendance_record_id, format=None):
        try:
            # Load the trained model
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_filename = os.path.join(base_dir, 'analytics/ml_models/student_churn_model.pkl')
            clf = joblib.load(model_filename)

            # get student id from attendance record
            student_id = AttendanceRecord.objects.get(id=attendance_record_id).student.id

            # get student by id
            student = Students.objects.annotate(
                most_recent_present=Max(
                    'attendancerecord__attendance_reverse_relationship__date',
                    filter=Q(attendancerecord__status=3)
                )
                ).get(id=student_id)

            # clean and normalize the data for the student
            cleaned_normalized_data = clean_normalize_data(student)
            combined_data = cleaned_normalized_data['attendance'] + [cleaned_normalized_data['age_at_most_recent_present']]

            # convert to numpy array and reshape for prediction
            attendance_data = np.array(combined_data).reshape(1, -1)  # Reshape for a single sample

            # make prediction
            prediction = clf.predict(attendance_data)

            # add student to AtRiskStudents if prediction is 0 (predicted to quit)
            if prediction[0] == 0:
                # check if student is already in AtRiskStudents
                at_risk_student, created = AtRiskStudents.objects.get_or_create(student=student)
            else:
                # remove student from AtRiskStudents if prediction is 1 (predicted to be active)
                AtRiskStudents.objects.filter(student=student).delete()

            data = {
                'status': 'HTTP_200_OK',
                # 'student_id': student.id,
                # 'last_name': student.last_name_romaji,
                # 'first_name': student.first_name_romaji,
                # 'prediction': prediction[0],
                # 'attendance_data': attendance_data,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        