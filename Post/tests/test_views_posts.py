from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed
from Post.views import get_post_by_query_text


class TestViews:
    @pytest.mark.django_db
    def test_view_posts_GET(self, client):
        response = client.get(reverse('view posts'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'Post/postList.html')

    @pytest.mark.parametrize(
        "query_text, expected_output",
        [
            ("Sea", ["Dead Sea", "Sea of Galilee", "Eilat"]),
            ("beautiful", ["Dead Sea", "Eilat"]),
            ("nice", ["`En Yorqe`am"]),
            ("place", ["`En Yorqe`am", "Eilat", "Dead Sea"]),
            ("Tal aviv", []),
            ("", ["Dead Sea", "Sea of Galilee", "Eilat", "`En Yorqe`am"]),
        ],
    )
    @pytest.mark.django_db
    def test_post_exists_after_query(self, query_text, expected_output):
        posts = get_post_by_query_text(query_text)
        assert all(post.nameOfLocation in expected_output for post in posts)

    # assert all(course.location in expected_output for course in courses)

    @pytest.mark.django_db
    def test_verify_respone_GET(self, client):
        response = client.get(reverse('post_list_Search'), {'query_text': 'Galilee'})
        posts_not_found = [b'Eilat', b'Dead Sea', b'`En Yorqe`am']
        assert response.status_code == 200
        assert b'Galilee' in response.content
        assert all(post not in response.content for post in posts_not_found)
