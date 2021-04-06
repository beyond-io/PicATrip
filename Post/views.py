from .models import post
from django.views.generic import ListView


class PostListView(ListView):
    model = post
    template_name = 'Post/postsList.html'
    context_object_name = 'posts'
