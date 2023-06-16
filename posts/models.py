from django.db import models
from django.contrib.auth import get_user_model

from users.models import SubTier

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=32, null=True)
    images = models.ImageField(upload_to='images/', null=True, blank=True)
    attachments = models.FileField(upload_to='attachments/', null=True, blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'Post {self.pk}'
