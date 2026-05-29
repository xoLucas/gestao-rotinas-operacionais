from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.accounts.models import OperatorProfile


User = get_user_model()


class OperatorProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source="get_role_display", read_only=True)
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = OperatorProfile
        fields = [
            "id",
            "role",
            "role_display",
            "team",
            "team_name",
            "registration_number",
            "is_active",
        ]


class CurrentUserSerializer(serializers.ModelSerializer):
    operator_profile = OperatorProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "operator_profile",
        ]