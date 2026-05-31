from rest_framework import serializers
from django.utils import timezone

from apps.operations.models import OperationalArea, Asset
from apps.routines.models import Routine, RoutineStep
from apps.scheduling.models import Shift, ScheduleRule
from apps.execution.models import RoutineExecution, ExecutionStepResult


class OperationalAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationalArea
        fields = [
            "id", "name", "description", "latitude", 
            "longitude", "radius_meters", "requires_authorization"
        ]


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "tag", "name", "asset_type", "area"]


class RoutineStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineStep
        fields = [
            "id", "order", "title", "description", 
            "is_required", "requires_photo", "requires_value_input"
        ]


class RoutineSerializer(serializers.ModelSerializer):
    # Aninhamos os steps para que o mobile receba a rotina e seus checklists de uma vez só
    steps = RoutineStepSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        fields = [
            "id", "name", "instruction", "category", "criticality",
            "area", "route", "asset", "requires_photo",
            "requires_geolocation", "requires_observation",
            "can_generate_service_request", "priority", "steps"
        ]


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ["id", "name", "start_time", "end_time"]


class ScheduleRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleRule
        fields = [
            "id", "routine", "shift", "frequency_type", "interval_hours",
            "fixed_time", "monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday", "window_before_minutes",
            "window_after_minutes"
        ]

class SyncStepResultSerializer(serializers.Serializer):
    step_id = serializers.IntegerField()
    is_completed = serializers.BooleanField(default=False)
    observation = serializers.CharField(allow_blank=True, required=False)
    value = serializers.CharField(allow_blank=True, required=False)

class SyncExecutionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=RoutineExecution.Status.choices)
    started_at = serializers.DateTimeField(allow_null=True, required=False)
    completed_at = serializers.DateTimeField(allow_null=True, required=False)
    observation = serializers.CharField(allow_blank=True, required=False)
    outside_geofence_justification = serializers.CharField(allow_blank=True, required=False)
    has_abnormality = serializers.BooleanField(default=False)
    
    # Lista de resultados das etapas aninhada
    steps = SyncStepResultSerializer(many=True, required=False)