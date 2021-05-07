from django.db import migrations, transaction
from django.contrib.auth.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('users', '__latest__'),
        ('Post', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from Post.models import Post

        users_list = [
            User.objects.create_user('Shoval', 'Test10@gmail.com', 'password777'),
            User.objects.create_user('Daniel', 'Test20@gmail.com', 'password777'),
        ]

        Post_list = [
            Post(
                nameOfLocation='Eilat',
                photoURL="https://israel.travel/wp-content/uploads/2019/02/eilatnewinside-min.jpg",
                Description='This is my favorite place! chill vibes and beautiful sea.',
            ),
            Post(
                nameOfLocation='Dead Sea',
                photoURL="https://velvetescape.com/wp-content/uploads/2011/11/IMG_2370-3-1280x920.jpg",
                Description='Beautiful place.',
            ),
        ]

        test_data = list(zip(users_list, Post_list))

        with transaction.atomic():

            for user, post in test_data:
                user.save()
                post.user = user
                post.save()

    operations = [migrations.RunPython(generate_data)]
