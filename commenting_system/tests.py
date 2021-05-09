import pytest
from django.contrib.auth.models import User
from commenting_system.models import Comment
from Post.models import Post


@pytest.fixture
@pytest.mark.django_db
def user_list():
    teardown_user_list()
    username = 'Test-user{}'
    email = '{}@gmail.com'
    password = '{}password'
    num_of_users = 5
    return [
        User.objects.create_user(
            username.format(ind),
            email.format("test-" + str(ind)),
            password.format("test-" + str(ind)),
        )
        for ind in range(num_of_users)
    ]


def teardown_user_list():
    User.objects.all().delete()


@pytest.fixture
def place_choices():
    return [
        'Eilat',
        'The Dead Sea',
        'The See of Galilee',
        'Ben-Shemen Forest',
        'Monfort Lake',
    ]


@pytest.fixture
def post_list(user_list, place_choices):

    return [
        Post(
            user=user_list[i],
            nameOfLocation=place_choices[i],
            photoURL=f'www.test_{i + 1}.com',
            Description=f'This is my #{i + 1} favorite place! chill vibes and beautiful view.',
        )
        for i in range(0, 5)
    ]


@pytest.fixture
def body_list():
    return [
        'first comment test only letters and spaces',
        '~!@#$%^&*()_+/*-.:/<>;{}[]=`',
        'test body. including special characters:!@#$%? and letters',
        'test body with more lines in body-' + (5 * 'test \n') + 'test.',
        'test body with long lines in body-' + (8 * 'test - ') + 'test',
    ]


@pytest.fixture
def label_list():
    return ["Recommended", "Want to go", "Quiet", "Crowded", "Chance to meet"]


@pytest.fixture
@pytest.mark.django_db
def parameters_list(user_list, post_list, body_list, label_list):
    return list(zip(user_list, post_list, body_list, label_list))


@pytest.mark.django_db
def test_create_comment(parameters_list):
    for user, post, body, label in parameters_list:
        new_comment = Comment(user=user, post=post, body=body, label=label)
        assert new_comment is not None
        assert isinstance(new_comment, Comment)


@pytest.mark.django_db
def test_comment_is_active_after_approving(parameters_list):
    for user, post, body, label in parameters_list:
        new_comment = Comment(user=user, post=post, body=body, label=label)
        new_comment.approve()
        assert new_comment.active is True


@pytest.mark.django_db
def test_comment_is_not_active_by_default(parameters_list):
    for user, post, body, label in parameters_list:
        new_comment = Comment(user=user, post=post, body=body, label=label)
        assert new_comment.active is False


@pytest.mark.django_db
def test_add_comment(parameters_list):
    for user, post, body, label in parameters_list:
        post.save()
        new_comment = Comment(user=user, post=post, body=body, label=label)
        new_comment.save()
        added_comment = Comment.objects.get(user=user)
        assert added_comment is not None
        assert isinstance(added_comment, Comment)
        assert added_comment == new_comment
    teardown_test_add_comment()


def teardown_test_add_comment():
    User.objects.all().delete()
    Post.objects.all().delete()
    Comment.objects.all().delete()


@pytest.mark.django_db
def test_remove_comment(parameters_list, user_list, post_list):
    for user, post, body, label in parameters_list:
        post.save()
        new_comment = Comment(user=user, post=post, body=body, label=label)
        new_comment.save()

    Comment.objects.all().delete()
    assert all(Comment.objects.filter(user=user).count() == 0 for user in user_list)
    assert all(
        User.objects.get(username=user.username) is not None for user in user_list
    )
    assert all(User.objects.get(username=user.username) == user for user in user_list)
    assert all(Post.objects.get(user=user) is not None for user in user_list)
    assert all(
        Post.objects.get(user=user) == post for post in post_list if post.user == user
    )
    teardown_remove_comment()


def teardown_remove_comment():
    User.objects.all().delete()
    Post.objects.all().delete()


@pytest.mark.django_db
def test_str(parameters_list):
    for user, post, body, label in parameters_list:
        new_comment = Comment(user=user, post=post, body=body, label=label)
        assert (
            str(new_comment)
            == f'Comment {body} by {user.username} at {new_comment.created_on} using label:{label}'
        )
