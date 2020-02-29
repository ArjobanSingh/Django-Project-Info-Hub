from django.urls import path
from .views import blog_list, BlogDetailView, BlogCreateView,  blog_delete, blog_update, following_posts

urlpatterns=[
    path('', blog_list, name='home'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('post/new/',BlogCreateView.as_view(), name="post_new"),
    path('posts/following', following_posts, name='foolowing_posts'),

    #path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name="post_edit"),
    #path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name="post_delete"),

    path('post/<int:pk>/edit/', blog_update, name="post_edit"),
    path('post/<int:pk>/delete/', blog_delete, name="post_delete"),
]