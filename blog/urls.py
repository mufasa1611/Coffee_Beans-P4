from django.urls import path
from .views import PostList, post_detail
from . import views

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('favorite/<int:post_id>/', views.favorite, name='favorite'),  
    path('favorites/', views.favorites_list, name='favorites_list'),   
    path('<slug:slug>/edit_comment/<int:comment_id>/', views.comment_edit, name='comment_edit'),
    path('<slug:slug>/delete_comment/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('<slug:slug>/', post_detail, name='post_detail'), 
]
