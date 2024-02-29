from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from .forms import PostCreateForm, CommentCreateForm
from .models import Post, Category, User, Profile, Like, Follow, Comment


# Create your views here.

def pagination(req, post):
    paginator = Paginator(post, 5)  # что делим, сколько на 1 станице
    page_number = req.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    posts = Post.objects.all()
    page_obj = pagination(request, posts)
    context = {
        'page_obj': page_obj
    }
    template = 'blog/index.html'
    return render(request, template, context)


def post_info(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()
        is_follow = Follow.objects.filter(follower=request.user,
                                          author=post.author)
    else:
        is_liked = False
        is_follow = False

    likes = Like.objects.filter(post=post).count()
    form = CommentCreateForm(request.POST or None)
    comments = Comment.objects.filter(post=post)
    context = {
        'post': post,
        'is_liked': is_liked,
        'likes': likes,
        'is_follow': is_follow,
        'form': form,
        'comments': comments,
    }
    template = 'blog/post_info.html'
    return render(request, template, context)


def category_info(request, slug):
    """
    Функция отображения страницы с постами в определенной категории
    :param request: запрос
    :param slug: уникальное имя категории
    :return: HttpResponse
    """
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts
    }
    template = 'blog/category_info.html'
    return render(request, template, context)


def all_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    template = 'blog/all_categories.html'
    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = user.post.all()
    count = user.post.count()
    if request.user.is_authenticated:
        is_follow = Follow.objects.filter(author=user,
                                          follower=request.user).exists()
    else:
        is_follow = False
    user.follows_count = Follow.objects.filter(author=user).count()
    user.likes_count = Like.objects.filter(post__author=user).count()
    context = {
        'author': user,
        'posts': posts,
        'count': count,
        'is_follow': is_follow,

    }
    template = 'blog/profile.html'
    return render(request, template, context)


def search(request):
    query = request.GET.get('text')
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(text__icontains=query))
    profiles = Profile.objects.filter(
        Q(user__username__icontains=query) | Q(
            user__first_name__icontains=query) | Q(
            user__last_name__icontains=query))
    categories = Category.objects.filter(title__icontains=query)

    context = {
        'posts': posts,
        'categories': categories,
        'profiles': profiles,
    }
    template = 'blog/search.html'
    return render(request, template, context)


@login_required()
def add_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if not Like.objects.filter(post=post, user=request.user).exists():
        Like.objects.create(post=post, user=request.user)
    return redirect('blog:post_info', pk)


@login_required()
def del_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    like = Like.objects.filter(post=post, user=request.user)
    if like.exists():
        like.delete()
    return redirect('blog:post_info', pk)


@login_required
def add_sub(request, username):
    follower = request.user  # тот кто подписывается
    author = get_object_or_404(User, username=username)  # на кого
    if follower != author:
        if not Follow.objects.filter(follower=follower,
                                     author=author).exists():
            Follow.objects.create(follower=follower, author=author)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def del_sub(request, username):
    follower = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(follower=follower, author=author)
    if follow.exists():
        follow.delete()
    return redirect(request.META.get('HTTP_REFERER'))  # фишка


def likes_index(request):
    """В шаблон likes_index вывести посты,
    которые оценил пользователь, сделавший запрос"""
    # likes = Like.objects.filter(user=request.user)
    # # коннект между постом и лайком
    # # как из лайков получить список постов
    # posts = [like.post for like in likes]
    posts = Post.objects.filter(liked_post__user=request.user)
    page_obj = pagination(request, posts)
    context = {
        'page_obj': page_obj,
        'header': 'like',
    }
    template = 'blog/index.html'
    return render(request, template, context)


def follow_index(request):
    """В шаблон follow_index посты авторов, на которых
    подписан текущий пользователь"""
    posts = Post.objects.filter(author__flwg__follower=request.user)
    page_obj = pagination(request, posts)
    context = {
        'page_obj': page_obj,
        'header': 'news',
    }
    template = 'blog/index.html'
    return render(request, template, context)


def follow_list(request):
    """В шаблон follow_list авторов, на которых
        подписан текущий пользователь"""
    profiles = Profile.objects.filter(user__flwg__follower=request.user)
    context = {
        'profiles': profiles
    }
    template = 'blog/authors.html'
    return render(request, template, context)


class PostCreate(FormView):
    template_name = 'blog/create_post.html'  # шаблон
    form_class = PostCreateForm  # форма, которая должна выводится
    success_url = reverse_lazy('blog:index')  # ссылка, на которую

    # мы переходим в случае успеха

    def form_valid(self, form):
        print(form.cleaned_data)
        Post.objects.create(author=self.request.user, **form.cleaned_data)
        return redirect(self.success_url)


@login_required()
def create_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = CommentCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        Comment.objects.create(comment_author=request.user,
                               post=post,
                               **form.cleaned_data)
    return redirect('blog:post_info', pk)


class PostEdit(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = 'value'
        return context


