from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm, SubscribeForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache


class PostsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-published_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsList(PostsList):
    template_name = 'news.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="NW")


class ArticlesList(PostsList):
    template_name = 'articles.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="AR")


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class NewsDetail(PostDetail):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="NW")


class ArticleDetail(PostDetail):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="AR")


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsportal.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsCreate(PostCreate):
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NW'
        post.author = self.request.user.author
        # self.message_send(form, post)
        return super().form_valid(form)

    # def message_send(self, form, post):
    #
    #     for category in form.cleaned_data['category']:
    #         category_cur = Category.objects.get(category=category).users.all()
    #         for user in category_cur:
    #             html_content = render_to_string(
    #                 'post_message.html',
    #                 {
    #                     'post': post,
    #                     'user': user
    #                 }
    #             )
    #             msg = EmailMultiAlternatives(
    #                 subject=f"""New "{category}" post here - {form.cleaned_data['post_title']}""",
    #                 body=f"Hello, {user.username}! New post in your favorite section! {form.cleaned_data['post_text']}",
    #                 from_email='newspaper.main@yandex.ru',
    #                 to=[user.email],
    #             )
    #             msg.attach_alternative(html_content, "text/html")
    #             msg.send()


class ArticleCreate(PostCreate):
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        post.author = self.request.user.author
        return super().form_valid(form)


class PostSearch(PostsList):
    template_name = 'post_search.html'


class NewsSearch(PostSearch):
    template_name = 'news_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="NW")


class ArticleSearch(PostSearch):
    template_name = 'article_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs.filter(type="AR")


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class NewsEdit(PostEdit):
    template_name = 'news_edit.html'


class ArticleEdit(PostEdit):
    template_name = 'article_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    # def delete(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     cache.delete(f'product-{self.object.pk}')
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)


class NewsDelete(PostDelete):
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(PostDelete):
    template_name = 'article_delete.html'
    success_url = reverse_lazy('articles_list')


@login_required
def subscribe(request):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data['sub_category'])
        print(form.cleaned_data['rpath'])
        Category.objects.get(
            category=form.cleaned_data['sub_category']).users.add(request.user)
    return redirect(form.cleaned_data['rpath'])
