from datetime import date, timedelta
from django.db.models import Count, Max, Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os
# models
from attendance.models import AttendanceRecord
from students.models import Students
from analytics.models import AtRiskStudents
# machine learning imports
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# ========================== FUNCTIONS ==========================
# converts attendance records to binary data and normalizes the length of list
def clean_normalize_data(student):
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

    return {
            'attendance': attendance_data,
            'currently_active': 1 if currently_active else 0,
        }

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
            X = [entry['attendance'] for entry in cleaned_data]
            y = [entry['currently_active'] for entry in cleaned_data]

            # convert to numpy arrays
            X = np.array(X)
            y = np.array(y)




            # =================== SCIKIT-LEARN - TRAINING ===================
            # Split into train/test sets (optional but recommended)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Create and train the classifier
            clf = RandomForestClassifier(n_estimators=100, random_state=42)
            clf.fit(X_train, y_train)

            # Predict on test set
            y_pred = clf.predict(X_test)

            # Evaluate accuracy
            from sklearn.metrics import accuracy_score
            print("Accuracy:", accuracy_score(y_test, y_pred))



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
        
# PREDICT STUDENT CHURN USING RANDOM FOREST CLASSIFIER FOR SINGLE STUDENT
class StudentChurnModelPredictForSingleStudent(APIView):
    def get(self, request, student_id, format=None):
        try:
            # Load the trained model
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_filename = os.path.join(base_dir, 'analytics/ml_models/student_churn_model.pkl')
            clf = joblib.load(model_filename)

            # get student by id
            student = Students.objects.annotate(
                most_recent_present=Max(
                    'attendancerecord__attendance_reverse_relationship__date',
                    filter=Q(attendancerecord__status=3)
                )
                ).get(id=student_id)

            # clean and normalize the data for the student
            cleaned_normalized_data = clean_normalize_data(student)['attendance']

            # convert to numpy array and reshape for prediction
            attendance_data = np.array(cleaned_normalized_data).reshape(1, -1)  # Reshape for a single sample

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
        
# PREDICT STUDENT CHURN USING RANDOM FOREST CLASSIFIER FOR ATTENDANCE RECORD
class StudentChurnModelPredictForAttendanceRecord(APIView):
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
            cleaned_normalized_data = clean_normalize_data(student)['attendance']

            # convert to numpy array and reshape for prediction
            attendance_data = np.array(cleaned_normalized_data).reshape(1, -1)  # Reshape for a single sample

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
        
# PREDICT STUDENT CHURN USING RANDOM FOREST CLASSIFIER FOR ACTIVE STUDENTS
class StudentChurnModelPredictForActiveStudents(APIView):
    def get(self, request, format=None):
        try:
            # Load the trained model
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_filename = os.path.join(base_dir, 'analytics/ml_models/student_churn_model.pkl')
            clf = joblib.load(model_filename)

            # get cutoff date of 28 days ago
            cutoff_date = date.today() - timedelta(days=28)

            # get all students with more than 2 present attendance records and at least one present record within the last 28 days
            students = (
                Students.objects
                .annotate(
                    present_count=Count(
                        'attendancerecord',
                        filter=Q(attendancerecord__status=3)
                    ),
                    latest_present_record=Max(
                        'attendancerecord__attendance_reverse_relationship__date',
                        filter=Q(attendancerecord__status=3)
                    )
                )
                .filter(
                    present_count__gte=2,
                    latest_present_record__gte=cutoff_date
                )
            )

            # Prepare data for prediction
            attendance_data_list = [] # list to hold attendance data for each student
            student_data_list = [] # list to hold student data
            for student in students:

                # get all attendance records for the student
                attendance_records = (
                    AttendanceRecord.objects
                    .filter(student=student)
                    .order_by('attendance_reverse_relationship__date')
                    .select_related('status')
                    .prefetch_related('attendance_reverse_relationship')
                )

                attendance_data = [] # list to hold attendance data for the student
                for record in attendance_records:
                    if record.status.id == 3:
                        attendance_data.append(1)
                    else:
                        attendance_data.append(0)

                # normalize the length of attendance records
                normalized_attendance_record_length = 300
                if len(attendance_data) < normalized_attendance_record_length:
                    padding = [0] * (normalized_attendance_record_length - len(attendance_data))
                    attendance_data = padding + attendance_data

                # append the attendance data to the list
                attendance_data_list.append(attendance_data)

                # append student data to the list
                student_data_list.append({
                    'student_id': student.id,
                    'last_name_romaji': student.last_name_romaji,
                    'first_name_romaji': student.first_name_romaji,
                    'present_count': student.present_count,
                })

            # Convert to numpy array
            X = np.array(attendance_data_list)
            # Reshape for prediction
            X = X.reshape(X.shape[0], -1)  # Reshape to (n_samples, n_features)

            # Make predictions
            predictions = clf.predict(X)

            # combinge predictions with student data
            results = [
                {
                    'student_id': student_data['student_id'],
                    'last_name_romaji': student_data['last_name_romaji'],
                    'first_name_romaji': student_data['first_name_romaji'],
                    'present_count': student_data['present_count'],
                    'prediction': int(prediction),  # Convert to int for JSON serialization
                }
                for student_data, prediction in zip(student_data_list, predictions)
            ]

            data = {
                'results': results,
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)