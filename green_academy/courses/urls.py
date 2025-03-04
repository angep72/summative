from django.urls import path
from .views import (CourseListCreateView, 
EnrollmentCreateView,
CourseRetrieveView,  # New Retrieve view for a single course
 
EnrollmentListView,
CourseDetailUpdateView,  
CourseDetailDeleteView)

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveView.as_view(), name='course-retrieve'),
    path('courses/<int:pk>/update/', CourseDetailUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', CourseDetailDeleteView.as_view(), name='course-delete'),
    path('enrollments/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('students/<int:student_id>/enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
]