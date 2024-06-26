from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment

# Register model posts.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'status', 'author', 'created_on', 'updated_on')
    search_fields = ['title']
    list_filter = ('status',)
    

# Register comments model.
@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('post', 'author', 'content')
    
