from datetime import date, timedelta
from django.db.models import Count, Max, Min, Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os, json
# models
from attendance.models import AttendanceRecord
from students.models import Students
from analytics.models import StudentChurnModelTrainingHistory
# machine learning imports
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, confusion_matrix, accuracy_score
import joblib

# ========================== FUNCTIONS ==========================
def clean_normalize_data(student):
    # ============ STUDENT IS ACTIVE ============
    # converts attendance records to binary data and normalizes the length of list
    # students without an attendance record in the last 28 days are considered as having quit
    cutoff_date = date.today() - timedelta(days=28)

    # determine if the student has been present in the last 28 days
    currently_active = student.last_attendance_record_date > cutoff_date

    # ============ ATTENDANCE - RECENT ABSENCE RATE ============
    analysis_period = 12 # weeks

    counts = AttendanceRecord.objects.filter(
        student=student,
        attendance_reverse_relationship__date__gte=student.last_attendance_record_date - timedelta(days=analysis_period * 7)
    ).aggregate(
        total_count=Count('id'),
        absence_count=Count('id', filter=Q(status=4))
    )

    absence_rate = counts['absence_count'] / counts['total_count']

    # ============ AGE AT TIME OF MOST RECENT ATTENDANCE RECORD ============
    age_at_most_recent_attendance_record = 0

    if student.birthday:
        # calculates age in years at the time of most recent attendance record
        birthday = student.birthday
        present_date = student.last_attendance_record_date
        years = present_date.year - birthday.year
        # Adjust if the birthday hasn't occurred yet this year
        if (present_date.month, present_date.day) < (birthday.month, birthday.day):
            years -= 1
        age_at_most_recent_attendance_record = years

    # ============ ENROLLMENT MONTH - CYCLICAL ENCODING ============
    enrollment_month = student.first_attendance_record_date.month
    enrollment_month_sin = np.sin(2 * np.pi * enrollment_month / 12)
    enrollment_month_cos = np.cos(2 * np.pi * enrollment_month / 12)

    return {
            'absence_rate': absence_rate,
            'age_at_most_recent_attendance_record': age_at_most_recent_attendance_record,
            'currently_active': 1 if currently_active else 0,
            'enrollment_month_sin': enrollment_month_sin,
            'enrollment_month_cos': enrollment_month_cos,
        }

# TRAIN RANDOM FOREST CLASSIFIER ON STUDENT ATTENDANCE DATA (STUDENT CHURN)
class StudentChurnModelTrain(APIView):    
    def get(self, request, format=None):
        try:
            # ================ CLEANING DATA FOR ML ANALYSIS ================
            # data for ML analysis
            cleaned_data = []

            # Annotate each student with their most recent attendance date
            students = Students.objects.annotate(
                attendance_count=Count('attendancerecord'),
                last_attendance_record_date=Max('attendancerecord__attendance_reverse_relationship__date'),
                first_attendance_record_date=Min('attendancerecord__attendance_reverse_relationship__date'),
            ).filter(attendance_count__gte=2)

            for index, student in enumerate(students):
                data = clean_normalize_data(student)
                cleaned_data.append(data)
                print(f"========== [{index}] {student.last_name_romaji}, {student.first_name_romaji} ({student.id}) ==========")
                print(data)
                print("")

            # ============================ NUMPY ============================
            # extract features (X) and labels (y)
            X = [[data['absence_rate'], data['age_at_most_recent_attendance_record'], data['enrollment_month_sin'], data['enrollment_month_cos']] for data in cleaned_data]
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

            y_pred_proba = clf.predict_proba(X_test)[:, 1]
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

            # Save model training history
            training_history = StudentChurnModelTrainingHistory(
                model_name='Third Generation',
                notes=json.dumps({
                    'accuracy': accuracy_score(y_test, y_pred),
                    'f1_score': f1_score(y_test, y_pred, average='weighted'),
                    'precision': precision_score(y_test, y_pred, average='weighted'),
                    'recall': recall_score(y_test, y_pred, average='weighted'),
                    'roc_auc': roc_auc_score(y_test, y_pred_proba),
                    'confusion_matrix': {
                        'true_positives': int(tp),
                        'true_negatives': int(tn),
                        'false_positives': int(fp),
                        'false_negatives': int(fn),
                    },
                    'sample_sizes': {
                        'training': len(X_train),
                        'test': len(X_test),
                    },
                    'class_distribution': {
                        'active_count': int(np.sum(y == 1)),
                        'churned_count': int(np.sum(y == 0)),
                    },
                    'feature_importance': {
                        'absence_rate': float(clf.feature_importances_[0]),
                        'age_at_most_recent_attendance_record': float(clf.feature_importances_[1]),
                        'enrollment_month_sin': float(clf.feature_importances_[2]),
                        'enrollment_month_cos': float(clf.feature_importances_[3]),
                    },
                })
            )
            training_history.save()

            # print data from most recently trained model to console
            for data_point in training_history.__dict__.items():
                print(data_point)

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