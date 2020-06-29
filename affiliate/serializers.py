from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        if validated_data["password"] != validated_data["confirm_password"]:
            raise ValidationError(
                {'confirm_password': ['Wrong confirm password']}
            )

        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_staff = False
        user.is_active = True
        user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'confirm_password',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)
