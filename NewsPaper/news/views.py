from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Category
from .filters import PostFilter
from django_filters.views import FilterView
from .forms import NewsEditForm, NewsAddForm

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name ='news.html'
    context_object_name = 'news'
    paginate_by = 10
    def get_queryset(self):
        if len(self.kwargs):
            category = Category.objects.get(id=self.kwargs['category_id'])
            queryset = Post.objects.filter(categories=category).order_by('-time_create')
        else:
            queryset = Post.objects.order_by('-time_create')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'Authors').exists()
        context['categories'] = Category.objects.all()
        if len(self.kwargs):
            context['category_name'] = Category.objects.get(id=self.kwargs['category_id'])
        return context


class PostDetail(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'Authors').exists()
        return context

class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news_edit.html'
    form_class = NewsEditForm
    permission_required = ('news.change_post',)



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

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('')
    permission_required = 'news.delete_post'

class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news_add.html'
    form_class = NewsAddForm
    permission_required = 'news.add_post'