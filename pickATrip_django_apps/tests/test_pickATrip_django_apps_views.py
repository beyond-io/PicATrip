from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


class TestViews:
    def test_homepage_GET(self, client):
        response = client.get(reverse('homepage'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'pickATrip_django_apps/homepage.html')

    def test_about_GET(self, client):
        response = client.get(reverse('about'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'pickATrip_django_apps/about.html')
