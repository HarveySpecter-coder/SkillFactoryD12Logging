from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name ='news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')

class PostDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'onenews'