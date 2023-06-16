from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreatePostAPIView.as_view(), name='create_post'),
    path('users/<int:user_id>/posts/', UserPostsAPIView.as_view(), name='user_posts'),
    path('<int:post_id>/delete/', DeletePostAPIView.as_view(), name='delete_post'),
    path('<int:post_id>/like/', LikePostAPIView.as_view(), name='like_post'),
]
