import pytest
import uuid
from django.contrib.auth.models import User


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


@pytest.mark.django_db
def test_update_user(user):
    user.username = 'updated-username'
    assert user.username == 'updated-username'
    user.email = 'update@mail.com'
    assert user.email == 'update@mail.com'
