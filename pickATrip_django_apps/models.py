from django.db import models
from django.utils import timezone


# Need to be implemented by Amir/Shoval
class Post(models.Model):
    pass


class Comment(models.Model):
    # profile_image = models.ImageField(upload_to='pickATrip_django_apps/profileImages', blank=True)

    class Tag(models.TextChoices):
        RECOMMENDED = "Recommended"
        WANT_TO_GO = "Want to go"
        QUITE = "Quite"
        CHANCE_TO_MEET = "Chance to meet"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=50)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    # temporary- might be replaced in a field for supporting a button functionality in later versions
    tag = models.CharField(choices=Tag.choices, max_length=20, blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.username)
