import pytest
from users.models import Profile


@pytest.mark.django_db(transaction=True)
class TestProfile:
    def test_profie_created(cls):
        profile_list = Profile.objects.all()
        profiles_names = []

        for profile in profile_list:
            profiles_names.append(profile.user.username)
        assert profiles_names == [
            ('Test-user-comments1'),
            ('Test-user-comments2'),
            ('Test-user-profile3'),
            ('Test-user-profile4')
        ]
