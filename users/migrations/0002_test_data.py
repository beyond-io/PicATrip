from django.db import migrations, transaction
from django.contrib.auth.models import User


def generate_user_list():
    username = 'Test-user777'
    email = 'Test@gmail.com'
    password = 'password777'

    username2 = 'Test-user222'
    email2 = 'Test777@gmail.com'
    password2 = 'password777'

    return [User.objects.create_user(username, email, password),
            User.objects.create_user(username2, email2, password2)]


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from users.models import Profile

        users_list = generate_user_list()
        for user in users_list:
            user.save()

        profile_test_data = [
            (users_list[0], 'default.jpg', '2010-09-08'),
            (users_list[1], 'default.jpg', '2000-01-01')
        ]

        with transaction.atomic():
            for user, profile_image, profile_dob in profile_test_data:
                Profile(user=user, image=profile_image, dob=profile_dob).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
