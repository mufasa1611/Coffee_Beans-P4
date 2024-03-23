from django.contrib import admin
from .models import Comment


# Order comments
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'created_on', 'approved')
    ordering = ['post']  
    
admin.site.register(Comment, CommentAdmin)
