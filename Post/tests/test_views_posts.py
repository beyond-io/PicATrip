from django.urls import reverse
import pytest
from pytest_django.asserts import assertTemplateUsed


class TestViews:
    @pytest.mark.django_db
    def test_view_posts_GET(self, client):
        response = client.get(reverse('view posts'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'Post/postList.html')
