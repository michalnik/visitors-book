from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True, "style": {"input_type": "password"}}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
