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
            User.objects.create_user(
                'Test-user-comments1', 'Test3@gmail.com', 'password777'
            ),
            User.objects.create_user(
                'Test-user-comments2', 'Test4@gmail.com', 'password222'
            ),
        ]

        body_comments_list = [('First comment test'), ('Second comment test')]

        Post_list = [
            Post(
                nameOfLocation='Sea of Galilee',
                photoURL="https://www.shappo.co.il/Resize_Image.aspx?maxsize=400&img=/pictures/cards/big/36630.jpg",
                Description='Perfect!',
            ),
            Post(
                nameOfLocation="`En Yorqe`am",
                photoURL="https://cdn1.sipurderech.co.il/1200x800_fit_90/1403218722_121.jpeg",
                Description='Really nice place',
            ),
        ]

        test_data = list(zip(users_list, body_comments_list, Post_list))

        with transaction.atomic():

            for user, body, post in test_data:
                user.save()
                post.user = user
                post.save()
                Comment(
                    user=user, body=body, post=post, label="Recommended", active=True
                ).save()

    operations = [migrations.RunPython(generate_data)]
