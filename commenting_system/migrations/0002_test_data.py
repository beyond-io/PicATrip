from django.db import migrations, transaction
from django.contrib.auth.models import User
from Post.models import Post


def generate_body_list():
    body_list = [
        'first comment test',
        '~!@#$%^&*()_+/*-.:/<>;{}[]=`',
        'another comment test. including special characters:!@#$%?',
        'another comment test with a much more lines in body-' +
        (20 * 'test \n') + 'test.',
        'another comment test with a much larger line in body-' + (20 * 'test - ') + 'test']

    return body_list


def generate_user_list():
    username_format = 'Test-user{}'
    email_format = '{}@gmail.com'
    password_format = '{}password'

    return [User.objects.create_user(username_format.format(str(i)),
                                     email_format.format(str(i)),
                                     password_format.format(str(i))) for i in range(1, 6)]


def generate_post(ind):
    author_choices = ['Shoval', 'Maayan', 'Amir', 'Leead', 'Nadav']
    place_choices = ['Eilat', 'Tel-Aviv', 'The Dead Sea',
                     'The see of galilee', 'Ben shemen forest']
    URL_formatted = 'www.test_{}.com'.format(ind + 1)
    description_formatted = 'This is my #{} favorite place! chill vibes and beautiful sea.'.format(
        ind + 1)

    return Post(nameOfPoster=author_choices[ind], nameOfLocation=place_choices[ind],
                photoURL=URL_formatted, Description=description_formatted)


class Migration(migrations.Migration):
    dependencies = [
        ('commenting_system', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from commenting_system.models import Comment

        body_comments_list = generate_body_list()
        users_list = generate_user_list()
        for user in users_list:
            user.save()

        test_data = list(zip(users_list, body_comments_list))

        with transaction.atomic():
            for user, body in test_data:
                tag_values = ["Recommended", "Want to go",
                              "Quiet", "Crowded", "Chance to meet"]
                for i, tag in enumerate(tag_values):
                    post = generate_post(i)
                    post.save()
                    Comment(user=user, body=body, post=post,
                            tag=tag, active=True).save()

    operations = [
        migrations.RunPython(generate_data)
    ]
