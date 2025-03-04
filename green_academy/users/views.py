from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        try:
            # Try to save the user instance
            serializer.save()
        except IntegrityError as e:
            # Handle foreign key or unique constraint failures
            return Response({"detail": "User registration failed due to an integrity error."},
                             status=400)
        except ValidationError as e:
            # Handle validation errors
            return Response({"detail": "Validation error during user registration."},
                             status=400)
        except Exception as e:
            # Catch any other exception that might occur
            return Response({"detail": str(e)},
                             status=500)

        return Response(serializer.data, status=201)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            # Generate JWT token pair
            response = super().post(request, *args, **kwargs)
        except IntegrityError:
            # Handle integrity errors, e.g., invalid user or database issues
            return Response({"detail": "Token generation failed due to integrity error."}, status=400)
        except Exception as e:
            # Handle other possible errors
            return Response({"detail": "An unexpected error occurred during token generation."},
                             status=500)
        
        return response
