<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
>>>>>>> 121d478 (Initial Setup and Project Configuration for a Django Blog)
