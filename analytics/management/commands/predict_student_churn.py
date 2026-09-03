import os
import json
import joblib
import numpy as np
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db.models import Count, Max, Min

from attendance.models import AttendanceRecord
from students.models import Students
from analytics.models import StudentChurnModelTrainingHistory, StudentChurnPrediction
from analytics.views import clean_normalize_data


class Command(BaseCommand):
    help = 'Generate student churn predictions'

    def handle(self, *args, **options):
        try:
            # Load the trained model
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            model_filename = os.path.join(base_dir, 'analytics/ml_models/student_churn_model.pkl')

            if not os.path.exists(model_filename):
                self.stdout.write(self.style.ERROR('Model file not found. Please train the model first.'))
                return

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
                churn_probability = clf.predict_proba(features)[0][0]

                # Get the previous prediction to calculate trend
                previous_prediction = StudentChurnPrediction.objects.filter(
                    student=student
                ).order_by('-date_time_created').first()

                # Calculate trend
                trend = 'no_change'
                if previous_prediction:
                    if churn_probability > previous_prediction.churn_probability:
                        trend = 'up'
                    elif churn_probability < previous_prediction.churn_probability:
                        trend = 'down'

                student_data = {
                    'student_id': student.id,
                    'first_name': student.first_name_romaji,
                    'last_name': student.last_name_romaji,
                    'churn_probability': float(churn_probability),
                    'trend': trend,
                }

                predictions.append(student_data)
            self.stdout.write("=========================================")
            self.stdout.write(f"Run Date: {date.today()}")
            self.stdout.write(f"Number of Students: {len(predictions)}")

            # delete existing predictions
            StudentChurnPrediction.objects.all().delete()

            # bulk create new predictions
            StudentChurnPrediction.objects.bulk_create([
                StudentChurnPrediction(
                    student_id=pred['student_id'],
                    churn_probability=pred['churn_probability'],
                    trend=pred['trend'],
                )
                for pred in predictions
            ])

            self.stdout.write(self.style.SUCCESS('Successfully generated student churn predictions'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))