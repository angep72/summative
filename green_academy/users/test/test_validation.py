# tests/test_validation.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_invalid_user_registration():
    client = APIClient()
    url = reverse('user-register')
    data = {
        'username': '',  # Invalid: empty username
        'email': 'invalid-email',  # Invalid: malformed email
        'password': 'short',  # Invalid: short password
        'role': 'invalid-role',  # Invalid: invalid role
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert 'email' in response.data
    assert 'password' in response.data
    assert 'role' in response.data