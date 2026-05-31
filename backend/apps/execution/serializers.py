from rest_framework import serializers
from .models import WorkSession, RoutineExecution, ExecutionStepResult

class RoutineExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineExecution
        fields = [
            "id", "work_session", "routine", "claimed_by", "status",
            "planned_start_at", "planned_end_at", "claimed_at",
            "started_at", "completed_at", "observation",
            "outside_geofence_justification", "has_abnormality",
            "service_request_required"
        ]

class WorkSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSession
        fields = [
            "id", "operator", "shift", "device_id", "started_at",
            "ended_at", "start_latitude", "start_longitude"
        ]
        read_only_fields = ["operator", "started_at", "ended_at"]