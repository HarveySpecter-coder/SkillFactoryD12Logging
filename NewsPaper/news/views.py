from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post
from .filters import PostFilter
from django_filters.views import FilterView
from .forms import NewsEditForm, NewsAddForm

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name ='news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-time_create')
    paginate_by = 10


class PostDetail(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'news_edit.html'
    form_class = NewsEditForm


# class Test(ListView):
#     model = Post
#     template_name = 'search.html'
#     context_object_name = 'search'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
#         context['form'] = ExampleForm
#         return context
class Test2(FilterView):
    model = Post
    context_object_name = 'search'
    template_name = 'search.html'
    filterset_class = PostFilter

class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('')

class PostCreate(CreateView):
    model = Post
    template_name = 'news_add.html'
    form_class = NewsAddForm