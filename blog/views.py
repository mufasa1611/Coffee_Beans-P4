
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Post, Comment
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
            comment.approved = 0
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

    #  statement to debug
    #print("Post Detail View - Slug:", slug)
    #print("Number of comments:", comment_count)

    return render(request, "blog/post_detail.html", {
        "post": post, 
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    })

# edit comments
def comment_edit(request, slug, comment_id):
    if request.method == "POST":
        # Retrieve post and comment instances
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)

        # Print received form data for debugging
        print("Received form data:", request.POST)

        # Check if the current user is the author of the comment
        if comment.author != request.user:
           # Handle unauthorized access 
            messages.add_message(request, messages.ERROR, 'You are not authorized to edit this comment.')
            return redirect('post_detail', slug=slug)

        # Process the form data
        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = 0  # Set to 'pending'
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment updated successfully.')
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        else:
            # Print form errors for debugging
            print("Form errors:", comment_form.errors)

            # Handle invalid form submission 
            messages.add_message(request, messages.ERROR, 'Error updating comment. Please check the form data.')
    else:
        # Handle non-POST requests 
        messages.add_message(request, messages.ERROR, 'Invalid request method.')
    
    # print statement to debug
    print("Comment Edit View - Slug:", slug)
    print("Comment ID:", comment_id)

    # Redirect back to post detail page
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

 
    # delete comment
def comment_delete(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check the user is the author to the comment
    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))
