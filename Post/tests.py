from Post.models import Post
from .forms import CreatePostForm
from django.db.models.query import QuerySet
from commenting_system.models import Comment
from django.contrib.auth.models import User
import pytest
from django.urls import reverse
from Post.views import CreateNewPost, post_detail, PostListView


@pytest.mark.django_db
def test_post_str(post):

    assert str(post) == "Gad traveled The Dead Sea and wrote: beautiful place"


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
def post(create_user, create_post):

    user = create_user(username='Gad', email='password1234', password='Gad@mail.com')
    return create_post(
        user=user,
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
def test_failed_delete_post(client, create_user, create_post):

    first_user = create_user(
        username='Gad', email='Gad@mail.com', password='password1234'
    )
    second_user = create_user(
        username='Nevo', email='Nevo@mail.com', password='password5678'
    )

    client.login(username=second_user.username, password='password5678')

    post = create_post(
        user=first_user,
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
def test_delete_post(client, create_user, create_post):

    first_user = create_user(
        username='Gad', email='Gad@mail.com', password='password1234'
    )
    client.login(username='Gad', password='password1234')

    post = create_post(
        user=first_user,
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
def test_create_post(client, create_user):
    Post.objects.all().delete()

    first_user = create_user(
        username='Gad', email='Gad@mail.com', password='password1234'
    )

    client.login(username='Gad', password='password1234')

    response = client.post(
        reverse('createPost'),
        {
            'nameOfLocation': 'Dead Sea',
            'photoURL': 'www.test123.com',
            'Description': 'Amazing!',
        },
    )

    assert response.status_code == 302
    assert response.url == '/postList/'

    post = Post.objects.all()
    assert post[0].user == first_user
    assert post[0].nameOfLocation == 'Dead Sea'
    assert post[0].photoURL == 'www.test123.com'
    assert post[0].Description == 'Amazing!'

    assert response.resolver_match.func == CreateNewPost


@pytest.mark.django_db
def test_failed_create_post(client, create_user):

    first_user = create_user(
        username='Gad', email='Gad@mail.com', password='password1234'
    )
    first_user.save()

    client.logout()

    response = client.get(reverse('createPost'))

    assert response.status_code == 302
    assert response.url == '/login/?next=/createPost/'


@pytest.mark.django_db
def test_post_detail(client, create_user, create_post):

    first_user = create_user(
        username='Gad', email='Gad@mail.com', password='password1234'
    )
    client.login(username='Gad', password='password1234')

    post = create_post(
        user=first_user,
        nameOfLocation='Israel',
        photoURL='www.test.com',
        Description='cool place',
    )
    post.save()

    response = client.get(reverse('post_detail', kwargs={'post_id': post.id}))

    assert response.status_code == 200
    assert response.resolver_match.func == post_detail


@pytest.mark.django_db
def test_failed_post_detail(client, create_user, create_post):

    first_user = create_user(
        username='Gad', email='Gad@mail.com', password='password1234'
    )

    post = create_post(
        user=first_user,
        nameOfLocation='Israel',
        photoURL='www.test.com',
        Description='cool place',
    )
    post.save()

    response = client.get(reverse('post_detail', kwargs={'post_id': post.id}))

    assert response.status_code == 302
    assert response.url == f'/login/?next=/postList/{post.id}/'


@pytest.mark.django_db
def test_post_list(client):
    response = client.get(reverse('view posts'))
    assert response.resolver_match.func.__name__ == PostListView.as_view().__name__


@pytest.mark.django_db
def test_update_post(client, create_user, create_post):

    new_user = create_user(
        username='Shovalo', email='Test10@gmail.com', password='password777'
    )
    client.login(username='Shovalo', password='password777')

    post = create_post(
        user=new_user,
        nameOfLocation='Israel',
        photoURL='www.test.com',
        Description='cool place',
    )
    post.save()

    response = client.post(
        reverse('post_update', kwargs={'pk': post.id}),
        {
            'nameOfLocation': 'Dead Sea',
            'photoURL': 'www.test1.com',
            'Description': 'Amazing!',
        },
    )

    assert response.status_code == 302

    post.refresh_from_db()

    assert post.nameOfLocation == 'Dead Sea'
    assert post.photoURL == 'www.test1.com'
    assert post.Description == 'Amazing!'


@pytest.mark.django_db
def test_failed_update_post(client, create_user, create_post):

    first_user = create_user(
        username='Shovalo', email='Test10@gmail.com', password='password777'
    )
    second_user = create_user(
        username='Dvir', email='Dvir@gmail.com', password='password777'
    )
    second_user.save()

    client.login(username='Dvir', password='password777')

    post = create_post(
        user=first_user,
        nameOfLocation='Israel',
        photoURL='www.test.com',
        Description='cool place',
    )
    post.save()

    response = client.post(
        reverse('post_update', kwargs={'pk': post.id}),
        {
            'nameOfLocation': 'Dead Sea',
            'photoURL': 'www.test1.com',
            'Description': 'Amazing!',
        },
    )

    assert response.status_code == 403
