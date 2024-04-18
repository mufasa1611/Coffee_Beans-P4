from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post
from .forms import CommentForm
from django.contrib import messages

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/home.html"
    paginate_by = 6


def post_detail(request, slug):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted and awaiting for approval'
            )
            comment_form = CommentForm() 
            return redirect('post_detail', slug=post.slug)
        else:
            messages.add_message(
                request, messages.ERROR,
                'There was an error with your submission. Please try again.'
            )
   

    return render(request, "blog/post_detail.html", {
        "post": post, 
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    })
