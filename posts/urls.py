from django.urls import path
from posts.views import *


urlpatterns = [
    path('categories/',home,name='categories'),
    path('posts/<slug>',PostListView.as_view(),name='posts'),
    path('post/<slug>',post_detail, name='post_detail'),
    path('delete/<slug>', delete_post, name='delete_post'),
    path('edit/<slug>', edit_post, name='edit_post'),
    path('create/<slug>', create_post, name='create_post')

]