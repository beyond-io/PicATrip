from django.db import migrations, transaction
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('users', '0003_alter_profile_dob'),
    ]

    def generate_data(apps, schema_editor):
        users_list = [
            User.objects.create_user('Test-user-profile1', 'Test@gmail.com', 'password777'),
            User.objects.create_user('Test-user-profile2', 'Test2@gmail.com', 'password222')
        ]

        with transaction.atomic():
            for user in users_list:
                user.save()

    operations = [
        migrations.RunPython(generate_data),
    ]
