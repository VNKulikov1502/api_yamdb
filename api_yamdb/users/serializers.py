from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .constants import EMAIL_LEHGTH, MAX_LENGTH
from .models import User
from .validators import validate_username


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH,
        validators=[UnicodeUsernameValidator(), validate_username]
    )
    email = serializers.EmailField(
        max_length=EMAIL_LEHGTH
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH,
    )
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
