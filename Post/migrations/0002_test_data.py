from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('Post', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from Post.models import post

        p1_Author = 'Shoval'
        p1_Place = 'Eilat'
        p1_URL = 'www.test.com'
        p1_Description = 'This is my favorite place! chill vibes and beautiful sea.'

        p2_Author = 'Daniel'
        p2_Place = 'Dead Sea'
        p2_URL = 'www.test2.com'
        p2_Description = 'Beautiful place.'

        with transaction.atomic():
            post(nameOfPoster=p1_Author, nameOfLocation=p1_Place, photoURL=p1_URL, Description=p1_Description).save()
            post(nameOfPoster=p2_Author, nameOfLocation=p2_Place, photoURL=p2_URL, Description=p2_Description).save()

    operations = [
        migrations.RunPython(generate_data)
    ]
