from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


def check_username_exists(username: str) -> bool:
    try:
        get_user_model().objects.get(username=username)
    except get_user_model().DoesNotExist:
        return False
    else:
        return True


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        if validated_data["password"] != validated_data["confirm_password"]:
            raise ValidationError(
                {'confirm_password': ['Passwords do not match']}
            )

        if check_username_exists(validated_data['email']):
            raise ValidationError(
                {'email': [
                    f"Email {validated_data['email']} is already registered"
                ]}
            )

        user = get_user_model().objects.create(
            email=validated_data['email'],
            username=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_staff = False
        user.is_active = True
        user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'confirm_password',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
