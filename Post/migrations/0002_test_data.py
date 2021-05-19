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
            User.objects.create_user('Shoval', 'shoval@gmail.com', 'password777'),
            User.objects.create_user('Leead', 'Leead@gmail.com', 'password777'),
        ]
        profile_picture_list = [
            'profile_pics/profile_female.png',
            'profile_pics/avatar.jpg',
        ]
        users_profiles = list(zip(users_list, profile_picture_list))
        for user, image in users_profiles:
            user.profile.image = image
            user.profile.save()

        users_list.append(users_list[0])
        users_list.append(users_list[1])

        post_Description_list = [
            ('This is my favorite place! chill vibes and beautiful sea.'),
            (
                "Great sunsets and sunrises with views of the West Bank"
                "and the mountain range of the East Bank and Oaisis on the mountains slopes"
                "... breathtaking views and a very high level of Oxygen too. Beautiful place."
            ),
            (
                "En Gedi is the biggest oasis in Israel. It has springs and waterfalls, "
                "and flowing brooks at the foot of the cliffs, home to ibexes and rock hyraxes."
            ),
            (
                "Ramon Crater is the largest natural crater in the world, "
                "it is 40 km (25 miles) long, 10 km (6.2 miles) wide and 500 meters (1640 ft) deep, "
                "and is shaped like an elongated heart. In the picture is the Bereshit"
                "Hotel, set on a cliff at the edge of the Ramon Crater in the Negev Desert."
            ),
        ]
        photoURL_List = [
            ("https://israel.travel/wp-content/uploads/2019/02/eilatnewinside-min.jpg"),
            (
                "https://velvetescape.com/wp-content/uploads/2011/11/IMG_2370-3-1280x920.jpg"
            ),
            (
                "https://images.unsplash.com/photo-1464980704090-17359156b2f6?ixid="
                "MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
            ),
            (
                "https://israelforever.org/interact/blog/8.-Beresheet-Hotel-Mitzpe-Ramon-Israel-7-e1431897591414.jpg"
            ),
        ]
        nameOfLocation_List = ['Eilat', 'Dead Sea', 'En gedi', 'Ramon Crater']

        post_data = list(zip(nameOfLocation_List, photoURL_List, post_Description_list))
        Post_list = []
        for nameOfLocation, URL, description in post_data:
            Post_list.append(
                Post(
                    nameOfLocation=nameOfLocation, photoURL=URL, Description=description
                )
            )

        test_data = list(zip(users_list, Post_list))

        with transaction.atomic():
            for user, post in test_data:
                post.user = user
                post.save()

    operations = [migrations.RunPython(generate_data)]
