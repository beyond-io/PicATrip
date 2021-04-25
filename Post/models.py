from django.db import models


class post(models.Model):

    nameOfPoster = models.CharField(max_length=100)
    nameOfLocation = models.CharField(max_length=100)
    photoURL = models.TextField()
    Description = models.TextField()

    def __str__(self):
        txt = "{0} traveled {1} and wrote: {2}"

        return txt.format(self.nameOfPoster, self.nameOfLocation, self.Description)
