from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Category, Subscribers
from .filters import PostFilter
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from .forms import NewsEditForm, NewsAddForm

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string


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
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['is_author'] = user.groups.filter(name = 'Authors').exists()
        context['categories'] = Category.objects.all()

        if len(self.kwargs):
            context['category_name'] = Category.objects.get(id=self.kwargs['category_id'])
            if user.is_authenticated:
                context['user_subsсribed'] = user.subscribers_set.filter(news_category__new_category=context['category_name'])
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

    # прекрасно понимаю, что писать цикл здесь, да ещё при отправке формы глупо,
    # но это лишь для теста. Позже отрефачю
    # За массову рассылку яндекс отправил меня в бан на 24 часа :)
    def form_valid(self, form):
        news_category_added = form.cleaned_data['categories'].first()
        subscribers_to_this_category = Subscribers.objects.filter(news_category__new_category=news_category_added)
        user_names = list(subscribers_to_this_category.values_list('user__username', flat=True))
        user_emails = list(subscribers_to_this_category.values_list('user__email', flat=True))
        user_names_emails = dict(zip(user_emails, user_names))
        connection = get_connection()
        connection.open()
        emails = []
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        for recipient in user_names_emails:
            context = {'username': user_names_emails[recipient], 'title': title, 'text':text[0:51]}
            html_content = render_to_string('subscribers.html', context)
            email = EmailMultiAlternatives(
                subject=title,
                body=text,
                from_email='aleek.sedler@yandex.ru',
                to=[recipient]
            )
            email.attach_alternative(html_content, "text/html")
            emails.append(email)
        connection.send_messages(emails)
        connection.close()
        return super().form_valid(form)


@login_required
def subscribe(request):
    user = request.user
    category = Category.objects.get(new_category=request.GET.get('category_name'))
    if not Subscribers.objects.filter(user=user).exists():
        Subscribers.objects.create(user=user)
    else:
        obj_subscribe = Subscribers.objects.get(user=user)
        category.subscribers_set.add(obj_subscribe)

    return redirect('/news/category/' + str(category.pk))