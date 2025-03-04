# tests/test_error_handling.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_nonexistent_endpoint():
    client = APIClient()
    url = '/api/nonexistent/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND