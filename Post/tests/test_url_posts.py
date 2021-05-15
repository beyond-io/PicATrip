from django.urls import reverse, resolve
from Post.views import PostListView, post_detail, CreateNewPost, postListSearch


class TestUrls:
    def test_postList_url_is_resolved(self):
        url = reverse('view posts')
        assert resolve(url).func.view_class == PostListView

    def test_post_detail_url_is_resolver(self):
        url = reverse('post_detail', args=[1])
        assert resolve(url).func == post_detail

    def test_createPost_url_is_resolved(self):
        url = reverse('createPost')
        assert resolve(url).func == CreateNewPost

    def test_searchPost_url_is_resovled(self):
        url = reverse('post_list_Search')
        assert resolve(url).func == postListSearch
