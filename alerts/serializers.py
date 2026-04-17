from rest_framework import serializers
# models
from alerts.models import AttendanceAlert

# ====================================================================
# =================== OVERVIEW - ATTENDANCE ALERTS ===================
# ====================================================================

# ======= Attendance Serializer =======
class AttendanceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceAlert
        fields = "__all__"