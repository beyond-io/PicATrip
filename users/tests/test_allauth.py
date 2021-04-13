# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from requests.exceptions import HTTPError

# from django.conf import settings
from django.contrib.auth.models import User

# from django.core import mail
from django.test.client import RequestFactory
from django.test import override_settings
from django.urls import reverse
from allauth.account import app_settings as account_settings

# from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.socialaccount.providers.google.provider import GoogleProvider
from pytest_django.asserts import assertTemplateUsed
import pytest
from unittest import mock


@pytest.mark.django_db
# Using this annotation to ensure what settings defined for the tests of google sign-in features in this class
class GoogleTests(OAuth2TestsMixin):
    provider_id = GoogleProvider.id

    @pytest.fixture
    def given_name(self):
        return "Maayan"

    @pytest.fixture
    def family_name(self):
        return "Hadar"

    @pytest.fixture
    def name(self, given_name, family_name):
        return f'{given_name} {family_name}'

    @pytest.fixture
    def email(self):
        return "maayan.hadar@example.com"

    @pytest.fixture
    def verified_email_val(self):
        return repr(True).lower()

    @pytest.fixture
    def unverified_email_val(self):
        return repr(False).lower()

    @pytest.fixture
    def default_event_data_without_verified_email(family_name, name, email):
        return {
            "family_name": f'{family_name}',
            "name": f'{name}',
            "picture": "https://lh3.googleusercontent.com/a-/A"
            "Oh14GhRHk2sL-xgCAYTscap9ByHf_16PYyebVwRkI6l1g=s96-c-rg-br100",
            "locale": "en-US",
            "gender": "male",
            "email": f'{email}',
            "link": "https://google.com/206015976",
            "given_name": "%s",
            "id": "206015976",
        }

    @pytest.fixture
    def event_data_401_code(self):
        return {
            "error": {
                "errors": [
                    {
                        "domain": "global",
                        "reason": "authError",
                        "message": "Invalid Credentials",
                        "locationType": "header",
                        "location": "Authorization",
                    }
                ],
                "code": 401,
                "message": "Invalid Credentials",
            }
        }

    @pytest.fixture
    def verified_email_event_data(
        self, default_event_data_without_verified_email, verified_email_val
    ):
        complete_event_data = default_event_data_without_verified_email[
            "verified_email"
        ] = verified_email_val
        return complete_event_data

    @pytest.fixture
    def unverified_email_event_data(
        self, default_event_data_without_verified_email, unverified_email_val
    ):
        complete_event_data = default_event_data_without_verified_email[
            "verified_email"
        ] = unverified_email_val
        return complete_event_data

    @pytest.fixture
    def api_client(self):
        from rest_framework.test import APIClient

        return APIClient()

    @pytest.fixture
    def verified_mail_mocked_response(self, api_client, verified_email_event_data):
        return api_client.post('create-service', data=verified_email_event_data)

    @pytest.fixture
    def unverified_mail_mocked_response(self, api_client, unverified_email_event_data):
        return api_client.post('create-service', data=unverified_email_event_data)

        # Imitating a response returned by google API by
        # fabricating data partially and returning a json format string

    @override_settings(
        SOCIALACCOUNT_AUTO_SIGNUP=True,
        ACCOUNT_SIGNUP_FORM_CLASS=None,
        ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
    )
    @mock.patch("allauth.socialaccount.providers.google.views" ".requests")
    def test_google_complete_login_401(self, api_client, event_data_401_code):
        from allauth.socialaccount.providers.google.views import (
            GoogleOAuth2Adapter,
        )

        request = RequestFactory().get(
            reverse(self.provider.id + "_login"), dict(process="login")
        )

        adapter = GoogleOAuth2Adapter(request)
        app = adapter.get_provider().get_app(request)
        token = SocialToken(token="some_token")
        # How can I connect the response to the process here without defining the mock response with
        # patch and then assigning it as appeared here:
        '''LessMockedResponse was a class that inherites from MockedResponse
        class and overriding/adding a raise_for_status method that raises HTTPError
        when the status code is NOT 200-> here below:
        response_with_401 = LessMockedResponse(
            401,
            """
            {"error": {
              "errors": [{
                "domain": "global",
                "reason": "authError",
                "message": "Invalid Credentials",
                "locationType": "header",
                "location": "Authorization" } ],
              "code": 401,
              "message": "Invalid Credentials" }
            }""",
        )
        with patch(
                "allauth.socialaccount.providers.google.views" ".requests"
        ) as patched_requests:
            patched_requests.get.return_value = response_with_401'''
        # Mocking a response with 401 status code
        response_with_401 = api_client.post('create-service', data=event_data_401_code)
        with pytest.raises(HTTPError):
            adapter.complete_login(request, app, token)
            assert response_with_401.status_code == 401

    def test_username_based_on_email_address(
        self, email, verified_mail_mocked_response
    ):
        self.login(verified_mail_mocked_response)
        user = User.objects.get(email=email)
        assert user.username == "maayan.hadar"
        assert verified_mail_mocked_response.status_code == 201

    def test_email_verified(self, email, verified_mail_mocked_response):
        self.login(verified_mail_mocked_response)
        email_address = EmailAddress.objects.get(email=email, verified=True)
        assert (
            EmailConfirmation.objects.filter(email_address__email=email).exists()
            is False
        )
        account = email_address.user.socialaccount_set.all()[0]
        assert account.extra_data["given_name"] == "Maayan"
        assert verified_mail_mocked_response.status_code == 201

    @override_settings(
        SOCIALACCOUNT_AUTO_SIGNUP=True,
        ACCOUNT_SIGNUP_FORM_CLASS=None,
        ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
    )
    def test_user_signed_up_signal(self, verified_mail_mocked_response):
        sent_signals = []

        def on_signed_up(sender, request, user, **kwargs):
            sociallogin = kwargs["sociallogin"]
            assert sociallogin.account.provider == GoogleProvider.id
            assert sociallogin.account.user == user
            sent_signals.append(sender)
            user_signed_up.connect(on_signed_up)
            self.login(verified_mail_mocked_response)
            assert len(sent_signals) > 0
            assert verified_mail_mocked_response.status_code == 201

    # Testing email have no verification (no symmetric signature provided for email verification)
    @override_settings(
        SOCIALACCOUNT_AUTO_SIGNUP=True,
        ACCOUNT_SIGNUP_FORM_CLASS=None,
        ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
    )
    @override_settings(ACCOUNT_EMAIL_CONFIRMATION_HMAC=False)
    def test_email_unverified(self, email, unverified_mail_mocked_response):
        response = self.login(unverified_mail_mocked_response)
        email_address = EmailAddress.objects.get(email=email)
        assert email_address.verified is False
        assert (
            EmailConfirmation.objects.filter(email_address__email=email).exists()
            is False
        )
        assertTemplateUsed(
            response, "account/email/email_confirmation_signup_subject.txt"
        )
        assert unverified_mail_mocked_response.status_code == 201
        assert response.status_code == 201

    @override_settings(
        SOCIALACCOUNT_AUTO_SIGNUP=True,
        ACCOUNT_SIGNUP_FORM_CLASS=None,
        ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.MANDATORY,
    )
    def test_account_connect(self, email, verified_mail_mocked_response):
        user = User.objects.create(username="user", is_active=True, email=email)
        user.set_password("test")
        user.save()
        EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
        self.client.login(username=user.username, password="test")
        self.login(verified_mail_mocked_response, process="connect")
        # Check if we connected...
        assert (
            SocialAccount.objects.filter(user=user, provider=GoogleProvider.id).exists()
            is True
        )
        assert EmailAddress.objects.filter(user=user).count() == 1
        assert EmailAddress.objects.filter(user=user, email=email).count() == 1
        assert verified_mail_mocked_response.status_code == 201
