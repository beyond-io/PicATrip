from django import forms
from .models import Post
from django.utils.translation import gettext_lazy as _


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('nameOfLocation', 'photoURL', 'Description')
        labels = {
            'nameOfLocation': _('Location name'),
            'photoURL': _('photo URL'),
        }
