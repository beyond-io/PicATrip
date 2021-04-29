import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed
from django.contrib.auth.models import User


class TestViews:
    def test_register_POST(self, client):
        response = client.post(reverse('register'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')

    def test_register_GET(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/register.html')

    @pytest.mark.django_db
    def test_profile_GET(self, client):
        user = User.objects.create_user('Test-user', 'Test-user@mail.com', 'Password')
        client.login(username=user.username, password='Password')
        response = client.get(reverse('profile'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/profile.html')

    def test_profile_anonymous_GET(self, client):
        response = client.get(reverse('profile'))
        assert response.status_code == 302

    def test_login_GET(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/login.html')

    def test_logout_GET(self, client):
        response = client.get(reverse('logout'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'users/logout.html')
