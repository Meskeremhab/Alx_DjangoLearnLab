from django.db import models
from django.conf import settings
from django.urls import reverse

from django.contrib.auth.models import User 

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"
class Meta:
    ordering = ['-published_date']

def __str__(self):
        return self.title

def get_absolute_url(self):
        return reverse('post-detail', args=[self.pk])
