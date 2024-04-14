from django.contrib import admin
from .models import Post, Comment


# Order posts
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_on', 'status')
    ordering = ['-created_on'] 



# Register  models .
class CommentAdmin(admin.ModelAdmin):
    exclude = ('status',)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
    