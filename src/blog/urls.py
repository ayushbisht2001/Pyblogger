
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', blog_post_list_view),
    path('<str:slug>/', blog_post_detail_view,name="blogpost-detail"),
    path('<str:slug>/edit/', blog_post_update_view),
    path('<str:slug>/delete/', blog_post_delete_view),
    path('<str:slug>/ajax/post/',  blog_post_comment),
    path('likes/<str:slug>',  blog_post_likes,name='blog_likes'),
    path('dislikes/<str:slug>',  blog_post_dislikes,name='blog_dislikes'),
    path('replies/<str:slug>/',  blog_post_comment_reply, name='get_replies'),
    path('comment/reply/<str:slug>/', blog_get_reply, name='blog_reply'),
    path('comment/delete/<str:slug>/', delete_comments, name='del_comments'),
    path('comment/reply/delete/<str:slug>/', delete_replies, name='del_replies'),
]
