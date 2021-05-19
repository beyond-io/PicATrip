import pytest
from django.contrib.auth.models import User
from commenting_system.models import Comment
from .forms import CommentForm
from Post.models import Post
from datetime import datetime, timedelta
import mock


@pytest.fixture
def user_list():
    teardown_user_list()
    username = 'Test-user{}'
    email = '{}@gmail.com'
    password = '{}password'
    num_of_users = 6
    return [
        User.objects.create_user(
            username.format(ind),
            email.format("test-" + str(ind)),
            password.format("test-" + str(ind)),
        )
        for ind in range(num_of_users)
    ]


@pytest.mark.django_db
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
        'Jerusalem',
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
        for i in range(0, 6)
    ]


@pytest.fixture
def body_list():
    return [
        'first comment test only letters and spaces',
        '~!@#$%^&*()_+/*-.:/<>;{}[]=`',
        'test body. including special characters:!@#$%? and letters',
        'test body with more lines in body-' + (5 * 'test \n') + 'test.',
        'test body with long lines in body-' + (8 * 'test - ') + 'test',
        'testing empty label',
    ]


@pytest.fixture
def label_list():
    return ["Recommended", "Want to go", "Quiet", "Crowded", "Chance to meet", ""]


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


@pytest.mark.django_db
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


@pytest.mark.django_db
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


@pytest.fixture
@pytest.mark.django_db
def commented_post_list(parameters_list, user_list):
    commented_posts = []
    for _, post, body, label in parameters_list:
        post.save()
        commented_posts.append(post)
        for user in user_list:
            user.save()
            # Saving only users comments to posts that isn't their own
            if post.user != user:
                new_comment = Comment(user=user, post=post, body=body, label=label)
                new_comment.save()

    return commented_posts


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body, label",
    [
        ("Testing Recommended label counter 1", "Recommended"),
        ("Testing Recommended label counter 2", "Recommended"),
        ("Testing Want to go label counter 1", "Want to go"),
        ("Testing Want to go label counter 2", "Want to go"),
        ("Testing Quiet label counter 1", "Quiet"),
        ("Testing Quiet label counter 2", "Quiet"),
        ("Testing Crowded label counter 1", "Crowded"),
        ("Testing Crowded label counter 2", "Crowded"),
        ("Testing Chance to meet label counter 1", "Chance to meet"),
        ("Testing Chance to meet label counter 2", "Chance to meet"),
    ],
)
def test_label_count_addition(commented_post_list, body, label):
    for post in commented_post_list:
        # Adding a comment with label to a post
        label_count_before_addition = post.comments.filter(label=label).count()
        Comment(user=post.user, post=post, body=body, label=label).save()
        assert (
            post.comments.filter(label=label).count() == label_count_before_addition + 1
        )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "body, label",
    [
        ("Testing Recommended label counter 1", "Recommended"),
        ("Testing Recommended label counter 2", "Recommended"),
        ("Testing Want to go label counter 1", "Want to go"),
        ("Testing Want to go label counter 2", "Want to go"),
        ("Testing Quiet label counter 1", "Quiet"),
        ("Testing Quiet label counter 2", "Quiet"),
        ("Testing Crowded label counter 1", "Crowded"),
        ("Testing Crowded label counter 2", "Crowded"),
        ("Testing Chance to meet label counter 1", "Chance to meet"),
        ("Testing Chance to meet label counter 2", "Chance to meet"),
    ],
)
def test_label_count_subtraction(commented_post_list, body, label):
    for post in commented_post_list:
        # Adding a comment with label to a post
        label_count_before_subtraction = post.comments.filter(label=label).count()
        comment = Comment(user=post.user, post=post, body=body, label=label)
        comment.save()
        assert (
            post.comments.filter(label=label).count()
            == label_count_before_subtraction + 1
        )
        comment.delete()
        assert (
            post.comments.filter(label=label).count() == label_count_before_subtraction
        )


@pytest.mark.django_db
@pytest.fixture
def comment_form():
    body = "Very beautiful place!"
    label = "Recommended"
    return CommentForm(
        data={
            'body': body,
            'label': label,
        }
    )


@pytest.mark.django_db
def test_comment_form(comment_form, commented_post_list):
    comment = comment_form.save(commit=False)
    assert comment is not None
    comment.user = commented_post_list[0].user
    comment.post = commented_post_list[-1]
    comment.save()
    # check if the values from the form saved properly (into a the comment) and functions as comment.
    assert isinstance(comment, Comment)
    assert comment_form.is_valid()
    assert comment.body == "Very beautiful place!"
    assert comment.label == "Recommended"
    assert comment.post == commented_post_list[-1]
    assert comment.user == commented_post_list[0].user
    assert (
        str(comment)
        == f'Comment {comment.body} by {comment.user.username} at {comment.created_on} using label:{comment.label}'
    )


@pytest.mark.django_db
def test_comment_creation_time(parameters_list):
    # make "now" 2 months ago to generate a constant time for the test
    test_time = datetime.now() - timedelta(days=60)

    with mock.patch('django.utils.timezone.now') as mock_now:
        mock_now.return_value = test_time
        for user, post, body, label in parameters_list:
            user.save()
            post.save()
            comment = Comment(user=user, post=post, body=body, label=label)
            comment.save()
            assert comment.created_on == test_time
