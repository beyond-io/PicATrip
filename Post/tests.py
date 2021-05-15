from Post.models import Post
from .forms import CreatePostForm
from django.db.models.query import QuerySet
from commenting_system.models import Comment
from django.contrib.auth.models import User
import pytest
from django.urls import reverse
from django.test import TestCase
from Post.views import CreateNewPost


@pytest.mark.django_db
def test_post_str(post):

    post.save()
    assert str(post) == "Shovalo traveled The Dead Sea and wrote: beautiful place"


@pytest.mark.django_db
def test_post_form(form):
    post = form.save(commit=False)

    # check if the values from the form saved properly (into a the post).
    assert form.is_valid()
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
    assert all(isinstance(post.user, User) for post in posts)
    assert all(len(post.photoURL) > 0 for post in posts)


@pytest.mark.django_db
def test_post_comments():
    posts = Post.all_posts()

    for post in posts:
        assert isinstance(post.comments.all(), QuerySet)
        assert all(isinstance(comment, Comment) for comment in post.comments.all())


@pytest.fixture
def post():
    new_user = User.objects.create_user(
        username='Shovalo', email='Test10@gmail.com', password='password777'
    )
    new_user.save()

    return Post(
        user=new_user,
        nameOfLocation='The Dead Sea',
        photoURL='www.testPost.com',
        Description='beautiful place',
    )


@pytest.fixture
def form():

    location = 'Israel'
    photoURL = 'www.test.com'
    description = 'cool place'

    return CreatePostForm(
        data={
            'nameOfLocation': location,
            'photoURL': photoURL,
            'Description': description,
        }
    )


@pytest.mark.django_db
def test_failed_delete_post(client):

    user1 = User.objects.create_user(
        username='Gad', email='Test22@gmail.com', password='password2222'
    )
    user1.save()

    user2 = User.objects.create_user(
        username='Nevo', email='Test23@gmail.com', password='password2233'
    )
    user2.save()

    client.login(username='Nevo', password='password2233')

    post = Post(
        user=user1,
        nameOfLocation='Israel',
        photoURL='www.test.com',
        Description='cool place',
    )
    post.save()

    response = client.post(
        reverse('post_delete', kwargs={'pk': post.id}),
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_post(client):

    user3 = User.objects.create_user(
        username='Amit', email='Test24@gmail.com', password='password2244'
    )
    user3.save()

    client.login(username='Amit', password='password2244')

    post = Post(
        user=user3,
        nameOfLocation='Israel',
        photoURL='www.test.com',
        Description='cool place',
    )
    post.save()

    response = client.post(
        reverse('post_delete', kwargs={'pk': post.id}),
    )

    assert response.status_code == 302


@pytest.mark.django_db
class CreatePostTest(TestCase):
    def test_create_post(self):
        Post.objects.all().delete()

        new_user = User.objects.create_user(
            username='Roni', email='Test26@gmail.com', password='password2266'
        )
        new_user.save()

        self.client.login(username='Roni', password='password2266')

        response = self.client.post(
            reverse('createPost'),
            {
                'nameOfLocation': 'Dead Sea',
                'photoURL': 'www.test123.com',
                'Description': 'Amazing!',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/postList/')

        post = Post.objects.all()
        self.assertEqual(post[0].user, new_user)
        self.assertEqual(post[0].nameOfLocation, 'Dead Sea')
        self.assertEqual(post[0].photoURL, 'www.test123.com')
        self.assertEqual(post[0].Description, 'Amazing!')

        self.assertEqual(response.resolver_match.func, CreateNewPost)

    def test_failed_create_post(self):

        new_user = User.objects.create_user(
            username='Roni', email='Test26@gmail.com', password='password2266'
        )
        new_user.save()
        self.client.logout()

        response = self.client.get(reverse('createPost'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/createPost/')
