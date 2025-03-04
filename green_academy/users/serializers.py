from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password



User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add user role to the token payload, only if it exists
        if hasattr(user, 'role'):
            token['role'] = user.role
        
        return token
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, value):
        validate_password(value)  # Enforce password validation
        return value

    def create(self, validated_data):
        print(validated_data)  # Debugging line to see what is in validated_data

        # Ensure the password is provided
        password = validated_data.get('password')
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        # Remove the password from validated_data and create the user
        validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Ensure the password is hashed
        user.save()
        return user