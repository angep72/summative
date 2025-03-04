from typing import List, Dict, Any
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from django.db import IntegrityError
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from users.models import User
from django.core.exceptions import PermissionDenied
from .permissions import IsInstructorOrAdmin

class CourseRetrieveView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

# The view to create and list courses
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add role-based permission
    def perform_create(self, serializer):
        try:
            # Set the instructor to the currently authenticated user
            serializer.save(instructor=self.request.user)
        except IntegrityError:
            # If the course creation fails due to a foreign key issue (e.g., invalid user)
            return Response({"detail": "Failed to create course due to foreign key constraint error."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Return successful response with created course data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        # Catch other exceptions such as ValidationError
        if isinstance(exc, IntegrityError):
            return Response({"detail": "Integrity error occurred during course creation."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


# The view to update an existing course
class CourseDetailUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Check if the user is an admin or the instructor who created the course
        obj = super().get_object()
        if self.request.user != obj.instructor and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to edit this course.")
        return obj

    def perform_update(self, serializer):
        # Update the course details
        serializer.save()


# The view to delete an existing course
class CourseDetailDeleteView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Check if the user is an admin or the instructor who created the course
        obj = super().get_object()
        if self.request.user != obj.instructor and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this course.")
        return obj
class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Check if the current user is the instructor or an admin
        if self.request.user == serializer.instance.instructor or self.request.user.role == 'admin':
            try:
                # Attempt to save the updated course data
                serializer.save()
            except IntegrityError:
                return Response({"detail": "Failed to update course due to foreign key constraint error."},
                                 status=status.HTTP_400_BAD_REQUEST)
        else:
            raise permissions.PermissionDenied("You do not have permission to update this course.")

    def handle_exception(self, exc):
        # Handle IntegrityError
        if isinstance(exc, IntegrityError):
            return Response({"detail": "Integrity error occurred during course update."},
                             status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class EnrollmentCreateView(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Set the student to the currently authenticated user
            serializer.save(student=self.request.user)
        except IntegrityError:
            return Response({"detail": "Failed to enroll due to foreign key constraint error."},
                             status=status.HTTP_400_BAD_REQUEST)
        
        # Return successful response with enrollment data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        # Catch IntegrityError and handle it gracefully
        if isinstance(exc, IntegrityError):
            return Response({"detail": "Integrity error occurred during enrollment."},
                             status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            # Return enrollments for the current user
            return Enrollment.objects.filter(student=self.request.user)
        except IntegrityError:
            return Response({"detail": "Failed to retrieve enrollments due to foreign key constraint error."},
                             status=status.HTTP_400_BAD_REQUEST)

    def handle_exception(self, exc):
        # Handle IntegrityError when fetching enrollments
        if isinstance(exc, IntegrityError):
            return Response({"detail": "Integrity error occurred while fetching enrollments."},
                             status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
