import pytest
import uuid
from django.contrib.auth.models import User
from django.test import TestCase
from users.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def test_username():
    return 'Test-user'


@pytest.fixture
def test_email():
    return 'Test-user@mail.com'


@pytest.fixture
def user(test_username, test_email, test_password):
    return User.objects.create_user(test_username, test_email, test_password)


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


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


def test_with_authenticated_client(client, django_user_model):
    username = "admin"
    password = "123456"
    django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    response = client.get('/profile/')
    assert response.status_code == 200
    client.logout()
    response2 = client.get('/profile/')
    assert response2.status_code == 302


def test_no_authenticated_client(client, django_user_model):
    username = "admin"
    password = "123456"
    django_user_model.objects.create_user(username=username, password=password)
    response = client.get('/profile/')
    assert response.status_code == 302
    assert response.url == '/login/?next=/profile/'


def test_update_user(client, django_user_model):
    username = "Test-user"
    password = "123456"
    django_user_model.objects.create_user(username=username, password=password)
    client.username = 'updated-username'
    assert client.username == 'updated-username'
    client.email = 'update@mail.com'
    assert client.email == 'update@mail.com'


class TestForms(TestCase):
    def test_UserRegistrationForm(self):
        form_data = {
            'username': 'username',
            'email': 'Test@example.com',
            'password1': 'test-password',
            'password2': 'test-password',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_UserUpdateForm(self):
        form_data = {'username': 'username', 'email': 'Test@example.com'}
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ProfileUpdateForm(self):
        form_data = {'dob': '1995-04-08', 'image': 'profile_pics/profile_picture.jpg'}
        form = ProfileUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
