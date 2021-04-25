from django.db import models


class Post(models.Model):
    nameOfPoster = models.CharField(max_length=100)
    nameOfLocation = models.CharField(max_length=100)
    photoURL = models.TextField()
    Description = models.TextField()

    def __str__(self):
        return f'{self.nameOfPoster} traveled {self.nameOfLocation} and wrote: {self.Description}'
