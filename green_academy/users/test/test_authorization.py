# tests/test_authorization.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from courses.models import Course

@pytest.mark.django_db
def test_instructor_can_create_course():
    client = APIClient()
    instructor = User.objects.create_user(
        username='instructor',
        email='instructor@example.com',
        password='testpassword123',
        role='instructor',
    )
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
    assert Course.objects.count() == 1

@pytest.mark.django_db
def test_student_cannot_create_course():
    client = APIClient()
    student = User.objects.create_user(
        username='student',
        email='student@example.com',
        password='testpassword123',
        role='student',
    )
    client.force_authenticate(user=student)
    url = reverse('course-list-create')
    data = {
        'title': 'Introduction to Sustainability',
        'description': 'Learn the basics of environmental sustainability.',
        'instructor': student.id,
        'duration': '4 weeks',
        'accessibility_options': ['audio_description', 'closed_captions'],
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN