from django.urls import reverse, resolve
from pickATrip_django_apps.views import homepage, about


class TestUrls:

    def test_home_url_is_resolved(self):
        url = reverse('homepage')
        assert resolve(url).func == homepage

    def test_about_url_is_resolved(self):
        url = reverse('about')
        assert resolve(url).func == about
