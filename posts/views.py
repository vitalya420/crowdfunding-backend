from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer
from .permissions import IsSubscriber


class CreatePostAPIView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostsAPIView(APIView):
    def get(self, request, user_id):
        # Retrieve all posts created by the user
        posts = Post.objects.filter(created_by=user_id).order_by('-id')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeletePostAPIView(APIView):
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)


class LikePostAPIView(APIView):
    def post(self, request, post_id, format=None):
        try:
            post = Post.objects.get(id=post_id)
            user = request.user

            if user in post.liked_by.all():
                # User has already liked the post, so remove the like
                post.liked_by.remove(user)
                action = 'unliked'
            else:
                # User has not liked the post, so add the like
                post.liked_by.add(user)
                action = 'liked'

            post.save()
            return Response({'action': action}, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
