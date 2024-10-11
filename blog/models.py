from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import re

def clean_nbsp(text):
    return re.sub(r'&nbsp;', ' ', text)
 

STATUS = ((0, "Draft"), (1, "Published"))

class Post(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
             User, on_delete=models.CASCADE,
             related_name="posts")
    featured_image = CloudinaryField('image', default='placeholder')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
          ordering = ["-created_on"]

    def __str__(self):
          return f"{self.title}" # | written by {self.author}"



# Comment  model .

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now =True) 
    
    APPROVAL_STATUS = (
        (0, 'Pending'),
        (1, 'Approved'),
    )
    approved = models.IntegerField(choices=APPROVAL_STATUS, default=0)
   

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.author} on {self.post.title}"

    def save(self, *args, **kwargs):
        self.content = clean_nbsp(self.content)
        super().save(*args, **kwargs) 
 
 # toring the contact us messages.       
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"       
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"