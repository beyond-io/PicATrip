from django.db import models
from django.conf import settings
from Post.models import post


class Comment(models.Model):
    class Tag(models.TextChoices):
        RECOMMENDED = "Recommended"
        WANT_TO_GO = "Want to go"
        QUIET = "Quiet", "Quiet Place"
        CROWDED = "Crowded", "Crowded Place"
        CHANCE_TO_MEET = "Chance to meet"

    commented_post = models.ForeignKey(
        post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(choices=Tag.choices,
                           max_length=20, blank=True, null=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)
