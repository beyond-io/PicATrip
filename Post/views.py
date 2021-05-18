from django.views.generic import ListView, DeleteView
from commenting_system.forms import CommentForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = Post
    template_name = 'Post/postList.html'
    context_object_name = 'posts'


@login_required
def CreateNewPost(request):
    form = CreatePostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'The post has been created')
        return redirect('/postList/')
    else:
        form = CreatePostForm()
    return render(
        request, 'Post/createPost.html', {'form': form, 'title': 'Create post'}
    )


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'Post/deletePost.html'
    success_url = '/postList/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


@login_required
def post_detail(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    # Using only the last 5 (approved) comments (at most- if exist)
    comments = post.comments.order_by("-created_on")[:5]
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current User to the comment
            new_comment.user = request.user
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            comment_form = CommentForm()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(
        request,
        'Post/post_detail.html',
        {
            'title': 'Post detail',
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'label_to_badge_type': {
                "Recommended": "bg-success",
                "Quiet": "bg-secondary",
                "Crowded": "bg-warning",
                "Chance to meet": "bg-primary",
                "Want to go": "bg-info",
            },
            'label_to_post_comments_count': {
                "Recommended": post.comments.filter(label="Recommended").count(),
                "Quiet": post.comments.filter(label="Quiet").count(),
                "Crowded": post.comments.filter(label="Crowded").count(),
                "Chance to meet": post.comments.filter(label="Chance to meet").count(),
                "Want to go": post.comments.filter(label="Want to go").count(),
            },
        },
    )


def postListSearch(request):
    if request.method == "GET":
        query_text = request.GET.get('query_text')
        posts_list = get_post_by_query_text(query_text)
        if posts_list.count() == 0:
            messages.error(
                request,
                f' There is no match for {query_text}',
            )
        return render(request, 'Post/postList.html', {"posts": posts_list})


def get_post_by_query_text(query_text):
    return Post.objects.filter(
        nameOfLocation__icontains=query_text
    ) | Post.objects.filter(Description__icontains=query_text)
