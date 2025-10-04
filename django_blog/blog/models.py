<<<<<<< HEAD
# blog/models.py
from django.conf import settings
from django.db import models
=======
from django.db import models
from django.conf import settings
from django.urls import reverse
>>>>>>> 121d478 (Initial Setup and Project Configuration for a Django Blog)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
<<<<<<< HEAD
        settings.AUTH_USER_MODEL,  # Django’s User model
=======
        settings.AUTH_USER_MODEL,
>>>>>>> 121d478 (Initial Setup and Project Configuration for a Django Blog)
        on_delete=models.CASCADE,
        related_name='posts'
    )

<<<<<<< HEAD
    def __str__(self):
        return self.title
=======
class Meta:
    ordering = ['-published_date']

def __str__(self):
        return self.title

def get_absolute_url(self):
        return reverse('post-detail', args=[self.pk])
>>>>>>> 121d478 (Initial Setup and Project Configuration for a Django Blog)
