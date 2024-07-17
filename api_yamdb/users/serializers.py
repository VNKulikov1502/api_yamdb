from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .constants import EMAIL_LEHGTH, MAX_LENGTH
from .models import User
from .validators import validate_username
from .enums import UserRoles

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
            'role'
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        
        # Здесь нужно обновлять группы, чтобы изменить роль
        role = validated_data.get('role')
        if role:
            if role == UserRoles.user.value:
                instance.groups.set([UserRoles.user.value])
            elif role == UserRoles.moderator.value:
                instance.groups.set([UserRoles.moderator.value])
            elif role == UserRoles.admin.value:
                instance.groups.set([UserRoles.admin.value])
        
        instance.save()
        return instance
