# tests/test_authentication.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User

@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = reverse('user-register')
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'role': 'student',
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert User.objects.get().username == 'testuser'

@pytest.mark.django_db
def test_user_login():
    client = APIClient()
    User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123',
        role='student',
    )
    url = reverse('token_obtain_pair')
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data