from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accounts.models import OperatorProfile
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


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

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Usuário ou senha inválidos.")

        if not user.is_active:
            raise serializers.ValidationError("Usuário inativo.")

        token, created = Token.objects.get_or_create(user=user)

        attrs["user"] = user
        attrs["token"] = token.key

        return attrs