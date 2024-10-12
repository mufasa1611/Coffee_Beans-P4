from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.views import generic
from blog.models import Post,Favorite, Comment, ContactMessage  
from .forms import CommentForm, ContactForm
from django.contrib import messages


# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1)
    template_name = "blog/home.html"
    paginate_by = 6
 
def post_detail(request, slug):
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, post=post).exists()
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

    return render(request, "blog/post_detail.html", {
        "post": post, 
        'is_favorited': is_favorited,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    })

# edit comments
def comment_edit(request, slug, comment_id):
    if request.method == "POST":
        post = get_object_or_404(Post, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author != request.user:
            messages.add_message(request, messages.ERROR, 'You are not authorized to edit this comment.')
            return redirect('post_detail', slug=slug)

        comment_form = CommentForm(data=request.POST, instance=comment)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.approved = 0  
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment updated successfully.')
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment. Please check the form data.')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid request method.')
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def comment_delete(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Thank you for your message!')
            return redirect('contact')  
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})
               
@login_required
def favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
    if not created:
        favorite.delete()  
    return redirect('post_detail', slug=post.slug)

@login_required
def favorites_list(request):
    user_favorites = request.user.favorites.all() 
    return render(request, 'blog/favorites_list.html', {'favorites': user_favorites})
