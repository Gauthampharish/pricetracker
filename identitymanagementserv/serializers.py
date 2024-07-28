from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model. This serializer handles the creation of new users
    and validation of username and email fields to ensure uniqueness.
    """

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create a new user with the validated data.

        Args:
            validated_data (dict): The validated data for creating a new user.

        Returns:
            User: The newly created user instance.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def validate_username(self, value):
        """
        Validate that the username is unique.

        Args:
            value (str): The username to validate.

        Raises:
            serializers.ValidationError: If the username already exists.

        Returns:
            str: The validated username.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        """
        Validate that the email is unique.

        Args:
            value (str): The email to validate.

        Raises:
            serializers.ValidationError: If the email already exists.

        Returns:
            str: The validated email.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. This serializer handles the validation of username
    and password for authentication.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the username and password for authentication.

        Args:
            data (dict): The data containing username and password.

        Raises:
            serializers.ValidationError: If the authentication fails.

        Returns:
            dict: The validated data.
        """
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        return data