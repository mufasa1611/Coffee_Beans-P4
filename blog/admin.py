from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment

# Register model posts.
@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'author', 'created_on', 'updated_on')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)

# Register comments model.
@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('post', 'status', 'author', 'content')
    exclude = ('status',)
