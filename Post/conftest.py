import pytest
from django.contrib.auth.models import User
from Post.models import Post


@pytest.fixture()
def create_user():
    def _create_user(**kwards):
        new_user = User.objects.create_user(
            username=kwards["username"],
            email=kwards["email"],
            password=kwards["password"],
        )
        return new_user

    return _create_user


@pytest.fixture()
def create_post():
    def _create_post(**kwards):
        new_post = Post(
            user=kwards["user"],
            nameOfLocation=kwards["nameOfLocation"],
            photoURL=kwards["photoURL"],
            Description=kwards["Description"],
        )
        return new_post

    return _create_post
