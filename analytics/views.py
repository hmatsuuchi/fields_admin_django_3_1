from datetime import date, timedelta
from django.db.models import Count, Max, Min, Q, Subquery, OuterRef, IntegerField
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import os, json
# models
from attendance.models import AttendanceRecord
from students.models import Students
from analytics.models import StudentChurnModelTrainingHistory, StudentChurnPrediction
# machine learning imports
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
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

    recent_absence_rate = counts['absence_count'] / counts['total_count'] if counts['total_count'] > 0 else 0.0

    # ============ ABSENCE RATE TREND ============
    # positive = getting worse, negative = getting better, 0 = no change
    lifetime_counts = AttendanceRecord.objects.filter(
        student=student
    ).aggregate(
        total_count=Count('id'),
        absence_count=Count('id', filter=Q(status=4))
    )

    lifetime_absence_rate = lifetime_counts['absence_count'] / lifetime_counts['total_count'] if lifetime_counts['total_count'] > 0 else 0.0

    absence_rate_trend = recent_absence_rate - lifetime_absence_rate

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

    # ============ TOTAL ATTENDANCE COUNT ============
    total_attendance_count = student.attendance_count

    # ============ TOTAL ENROLLMENT DURATION ============
    total_enrollment_duration = (student.last_attendance_record_date - student.first_attendance_record_date).days

    return {
        'recent_absence_rate': recent_absence_rate,
        'absence_rate_trend': absence_rate_trend,
        'age_at_most_recent_attendance_record': age_at_most_recent_attendance_record,
        'currently_active': 1 if currently_active else 0,
        'enrollment_month_sin': enrollment_month_sin,
        'enrollment_month_cos': enrollment_month_cos,
        'total_attendance_count': total_attendance_count,
        'total_enrollment_duration': total_enrollment_duration,
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
            ).filter(
                attendance_count__gte=2,
                last_attendance_record_date__isnull=False,
                first_attendance_record_date__isnull=False,
            )

            for index, student in enumerate(students):
                data = clean_normalize_data(student)
                cleaned_data.append(data)
                print(f"========== [{index}] {student.last_name_romaji}, {student.first_name_romaji} ({student.id}) ==========")
                print(data)
                print("")

            # ============================ NUMPY ============================
            # extract features (X) and labels (y)
            X = [[
                data['recent_absence_rate'],
                data['absence_rate_trend'],
                data['age_at_most_recent_attendance_record'],
                data['enrollment_month_sin'],
                data['enrollment_month_cos'],
                data['total_attendance_count'],
                data['total_enrollment_duration'],
            ] for data in cleaned_data]
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

            # Cross-validate on full dataset for reliable performance estimate
            cv_scores = cross_val_score(clf, X, y, cv=5, scoring='roc_auc')

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
                        'recent_absence_rate': float(clf.feature_importances_[0]),
                        'absence_rate_trend': float(clf.feature_importances_[1]),
                        'age_at_most_recent_attendance_record': float(clf.feature_importances_[2]),
                        'enrollment_month_sin': float(clf.feature_importances_[3]),
                        'enrollment_month_cos': float(clf.feature_importances_[4]),
                        'total_attendance_count': float(clf.feature_importances_[5]),
                        'total_enrollment_duration': float(clf.feature_importances_[6]),
                    },
                    'cross_validation': {
                        'cv_roc_auc_mean': float(cv_scores.mean()),
                        'cv_roc_auc_std': float(cv_scores.std()),
                        'cv_roc_auc_scores': [float(s) for s in cv_scores],
                    },
                })
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

# PREDICT STUDENT CHURN USING TRAINED RANDOM FOREST CLASSIFIER MODEL
class StudentChurnPredict(APIView):
    def get(self, request, format=None):
        try:
            # Load the trained model
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_filename = os.path.join(base_dir, 'analytics/ml_models/student_churn_model.pkl')

            if not os.path.exists(model_filename):
                return Response({'error': 'Model file not found. Please train the model first.'}, status=status.HTTP_404_NOT_FOUND)

            clf = joblib.load(model_filename)

            # fetch all active students
            students = Students.objects.annotate(
                attendance_count=Count('attendancerecord'),
                last_attendance_record_date=Max('attendancerecord__attendance_reverse_relationship__date'),
                first_attendance_record_date=Min('attendancerecord__attendance_reverse_relationship__date'),
            ).filter(
                attendance_count__gte=2,
                last_attendance_record_date__gte=date.today() - timedelta(days=28),
            )

            # Prepare data for prediction
            predictions = []
            for student in students:
                data = clean_normalize_data(student)
                features = np.array([[
                    data['recent_absence_rate'],
                    data['absence_rate_trend'],
                    data['age_at_most_recent_attendance_record'],
                    data['enrollment_month_sin'],
                    data['enrollment_month_cos'],
                    data['total_attendance_count'],
                    data['total_enrollment_duration'],
                ]])

                # make prediction using the trained model
                churn_probability = clf.predict_proba(features)[0][0]  # Probability of churning (currently active = 1, churning = 0)

                student_data = {
                    'student_id': student.id,
                    'first_name': student.first_name_romaji,
                    'last_name': student.last_name_romaji,
                    'churn_probability': float(churn_probability),
                }

                predictions.append(student_data)

                print(student_data)

            # delete existing predictions
            StudentChurnPrediction.objects.all().delete()

            # bulk create new predictions
            StudentChurnPrediction.objects.bulk_create([
                StudentChurnPrediction(
                    student_id=pred['student_id'],
                    churn_probability=pred['churn_probability'],
                )
                for pred in predictions
            ])

            return Response({'status': 'HTTP_200_OK', 'predictions': predictions}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)