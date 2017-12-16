from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import serializers
from ..models import User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

        extra_kwargs = {
                "password": {
                    "write_only": True
                }
            }
            
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(label="Email address", required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]

        extra_kwargs = {
                "password": {
                    "write_only": True
                }
            }

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]

        if not email and not username:
            raise ValidationError("A username or email is required to login.")

        user = User.objects.filter(
                Q(email=email) |
                Q(username=username)
            ).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again.")

        data["token"] = "SOME RANDOM TOKEN"
        return data