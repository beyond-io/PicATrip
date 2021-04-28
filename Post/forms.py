from django import forms
from .models import Post
from django.utils.translation import gettext_lazy as _


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('nameOfPoster', 'nameOfLocation', 'photoURL', 'Description')
        labels = {
            'nameOfPoster': _('Author'),
            'nameOfLocation': _('Location name'),
            'photoURL': _('photo URL'),
        }
