from django.db import models
from django.conf import settings
from Post.models import Post


class Comment(models.Model):
    class Label(models.TextChoices):
        RECOMMENDED = "Recommended"
        WANT_TO_GO = "Want to go"
        QUIET = "Quiet", "Quiet Place"
        CROWDED = "Crowded", "Crowded Place"
        CHANCE_TO_MEET = "Chance to meet"

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', null=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        null=False,
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    label = models.CharField(
        choices=Label.choices, max_length=20, blank=True, null=True
    )
    active = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.user.username} at {self.created_on} using label:{self.label}'

    def approve(self):
        self.active = True
