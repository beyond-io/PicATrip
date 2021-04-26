from Post.models import Post
from .forms import CreatePostForm
from django.db.models.query import QuerySet
from commenting_system.models import Comment
import pytest


@pytest.mark.django_db
def test_post_str(post):

    assert str(post) == "Shoval traveled The Dead Sea and wrote: beautiful place"


@pytest.mark.django_db
def test_post_form(form):

    post = form.save()

    # check if the values from the form saved properly (into a the post).
    assert form.is_valid()
    assert post.nameOfPoster == 'Daniel'
    assert post.nameOfLocation == 'Israel'
    assert post.photoURL == 'www.test.com'
    assert post.Description == 'cool place'


@pytest.mark.django_db
def test_post_creation(post):
    post.save()

    assert Post.objects.filter(pk=post.id).exists()  # checks if the post is saved
    assert Post.objects.get(pk=post.id) == post  # check if the post saved correctly


@pytest.mark.django_db
def test_post_delete(post):
    post.save()

    assert Post.objects.filter(pk=post.id).exists()
    Post.objects.get(pk=post.id).delete()
    assert Post.objects.filter(pk=post.id).exists() is False


@pytest.mark.django_db
def test_all_posts():

    posts = Post.all_posts()

    assert isinstance(posts, QuerySet)
    assert all(isinstance(post, Post) for post in posts)
    assert all(post is not None for post in posts)
    assert all(len(post.Description) > 0 for post in posts)
    assert all(len(post.nameOfLocation) > 0 for post in posts)
    assert all(len(post.nameOfPoster) > 0 for post in posts)
    assert all(len(post.photoURL) > 0 for post in posts)


@pytest.mark.django_db
def test_post_comments():
    posts = Post.all_posts()

    for post in posts:
        assert isinstance(post.comments.all(), QuerySet)
        assert all(isinstance(comment, Comment) for comment in post.comments.all())


@pytest.fixture
def post():

    return Post(
        nameOfPoster='Shoval',
        nameOfLocation='The Dead Sea',
        photoURL='www.testPost.com',
        Description='beautiful place',
    )


@pytest.fixture
def form():
    author = 'Daniel'
    location = 'Israel'
    photoURL = 'www.test.com'
    description = 'cool place'

    return CreatePostForm(
        data={
            'nameOfPoster': author,
            'nameOfLocation': location,
            'photoURL': photoURL,
            'Description': description,
        }
    )
