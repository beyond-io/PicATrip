import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user('Test-user', 'Test-user@mail.com', 'Password')


@pytest.mark.django_db
def test_user_creation(user):
    assert User.objects.filter(pk=user.id).exists()
    assert User.objects.get(pk=user.id) == user


@pytest.mark.django_db
def test_user_delete(user):
    assert User.objects.filter(pk=user.id).exists()
    User.objects.get(pk=user.id).delete()
    assert not User.objects.filter(pk=user.id).exists()


@pytest.mark.django_db
def test_should_not_check_unusable_password(user):
    user.set_unusable_password()
    assert not user.has_usable_password()


@pytest.mark.django_db
def test_login(user):
    c = Client()
    logged_in = c.login(username='Test-user', password='Password')
    assert logged_in
