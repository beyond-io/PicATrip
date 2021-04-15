from django.db import models
from django.urls import reverse


class Post(models.Model):
    nameOfPoster = models.CharField(max_length=100)
    nameOfLocation = models.CharField(max_length=100)
    photoURL = models.TextField()
    Description = models.TextField()

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'slug': self.slug})
