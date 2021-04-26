from django.urls import reverse, resolve
from users.views import register, profile
from django.contrib.auth.views import LoginView, LogoutView


class TestUrls:
    def test_register_url_is_resolved(self):
        url = reverse('register')
        assert resolve(url).func == register

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        assert resolve(url).func == profile

    def test_login_url_is_resolved(self):
        url = reverse('login')
        assert resolve(url).func.view_class == LoginView

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        assert resolve(url).func.view_class == LogoutView
