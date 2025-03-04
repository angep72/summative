# tests/test_integration.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from courses.models import Course, Enrollment

@pytest.mark.django_db
def test_course_creation_and_enrollment():
    client = APIClient()
    instructor = User.objects.create_user(
        username='instructor',
        email='instructor@example.com',
        password='testpassword123',
        role='instructor',
    )
    student = User.objects.create_user(
        username='student',
        email='student@example.com',
        password='testpassword123',
        role='student',
    )

    # Create a course
    client.force_authenticate(user=instructor)
    url = reverse('course-list-create')
    data = {
        'title': 'Introduction to Sustainability',
        'description': 'Learn the basics of environmental sustainability.',
        'instructor': instructor.id,
        'duration': '4 weeks',
        'accessibility_options': ['audio_description', 'closed_captions'],
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    course_id = response.data['id']

    # Enroll the student in the course
    client.force_authenticate(user=student)
    url = reverse('enrollment-create')
    data = {
        'student': student.id,
        'course': course_id,
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Enrollment.objects.count() == 1