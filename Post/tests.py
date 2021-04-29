from Post.models import Post
from .forms import CreatePostForm
import pytest


class TestPost:
    def test_post_creation(self):

        post1 = Post(
            nameOfPoster='Shoval',
            nameOfLocation='The Dead Sea',
            photoURL='www.testPost.com',
            Description='beautiful place',
        )

        assert str(post1) == "Shoval traveled The Dead Sea and wrote: beautiful place"


@pytest.mark.django_db
def test_post_form(form):

    post = form.save()

    # check if the values from the form saved properly (into a the post).
    assert form.is_valid()
    assert post.nameOfPoster == 'Daniel'
    assert post.nameOfLocation == 'Israel'
    assert post.photoURL == 'www.test.com'
    assert post.Description == 'cool place'


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
