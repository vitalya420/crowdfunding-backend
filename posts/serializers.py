from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    liked_by = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    available = serializers.SerializerMethodField()

    # text = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_liked_by(self, post):
        return len(post.liked_by.all())

    def get_is_liked(self, post):
        user = self.context['request'].user
        if user in post.liked_by.all():
            return True
        return False

    def get_available(self, post):
        user = self.context['request'].user
        return user.id == post.created_by.id or user.is_subscribed(post.created_by)

    def to_representation(self, instance):
        user = self.context['request'].user
        data = super().to_representation(instance)

        if not (user.id == instance.created_by.id or user.is_subscribed(instance.created_by)):
            data['text'] = None
        return data
