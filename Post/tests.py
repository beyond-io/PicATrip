from Post.models import Post


class TestPost():

    def test_post_creation(self):

        post1 = Post(nameOfPoster='Shoval',
                     nameOfLocation='The Dead Sea',
                     photoURL='www.testPost.com',
                     Description='beautiful place')

        assert str(post1) == "Shoval traveled The Dead Sea and wrote: beautiful place"
