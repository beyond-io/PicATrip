from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        null=False,
    )

    nameOfLocation = models.CharField(max_length=100)
    photoURL = models.TextField()
    Description = models.TextField()

    def __str__(self):
        return f'{self.user.username} traveled {self.nameOfLocation} and wrote: {self.Description}'

    @classmethod
    def all_posts(cls):
        return cls.objects.all()
