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
            User.objects.create_user("Ma'ayan", 'Leead@gmail.com', 'password777'),
            User.objects.create_user('Nadav', 'Nadav@gmail.com', 'password222'),
        ]

        body_comments_list = [
            (
                "Gorgeous views and calm waters. We took a short cruise here, complete with praise music"
                "and refreshments. This made for a refreshing stop made perfect by the warm sun and cool breeze."
                "Check beforehand to insure against inclement weather."
            ),
            (
                "Very nice chilling pool, but can be pretty much crowded on sunny days,"
                "as it is just a few hundred meters from parking - easy access."
            ),
        ]

        Post_list = [
            Post(
                nameOfLocation='Sea of Galilee',
                photoURL="https://www.shappo.co.il/Resize_Image.aspx?maxsize=400&img=/pictures/cards/big/36630.jpg",
                Description='It is the lowest freshwater lake on Earth and the second-lowest lake in the world',
            ),
            Post(
                nameOfLocation="`En Yorqe`am",
                photoURL="https://cdn1.sipurderech.co.il/1200x800_fit_90/1403218722_121.jpeg",
                Description='Beautiful spot with cool water',
            ),
        ]

        test_data = list(zip(users_list, body_comments_list, Post_list))

        with transaction.atomic():

            for user, body, post in test_data:
                user.save()
                post.user = user
                post.save()
                Comment(user=user, body=body, post=post, label="Recommended").save()

    operations = [migrations.RunPython(generate_data)]
