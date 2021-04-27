from django.db import migrations, transaction
from django.contrib.auth.models import User
from Post.models import Post


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('commenting_system', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from commenting_system.models import Comment

        users_list = [
            User.objects.create_user('Test-user-comments1', 'Test3@gmail.com', 'password777'),
            User.objects.create_user('Test-user-comments2', 'Test4@gmail.com', 'password222')
        ]

        body_comments_list = [
            ('First comment test'),
            ('Second comment test')
        ]

        Post_list = [
            Post(nameOfPoster='Leead', nameOfLocation='Eilat', photoURL='test_1.com', Description='Perfect!'),
            Post(nameOfPoster='Shoval', nameOfLocation='Tel-Aviv', photoURL='test_2.com', Description='This is nice'),
        ]

        test_data = list(zip(users_list, body_comments_list, Post_list))

        with transaction.atomic():

            for user, body, post in test_data:
                user.save()
                post.save()
                Comment(user=user, body=body, post=post,
                        label="Recommended", active=True).save()

    operations = [
        migrations.RunPython(generate_data)
    ]
