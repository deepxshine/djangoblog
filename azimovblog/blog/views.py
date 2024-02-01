from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Category, User, Profile, Like, Follow


# Create your views here.


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    template = 'blog/index.html'
    return render(request, template, context)


def post_info(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()
    else:
        is_liked = False
    likes = Like.objects.filter(post=post).count()
    context = {
        'post': post,
        'is_liked': is_liked,
        'likes': likes,
    }
    template = 'blog/post_info.html'
    return render(request, template, context)


def category_info(request, slug):
    """
    Функция отображения страницы с постами в определенной категории
    :param request: запрос)))
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
    follower = request.user # тот кто подписывается
    author = get_object_or_404(User, username=username) # на кого
    if follower != author:
        if not Follow.objects.filter(follower=follower, author=author).exists():
            Follow.objects.create(follower=follower, author=author)
    return redirect('blog:profile', username)


@login_required
def del_sub(request, username):
    follower = request.user
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(follower=follower, author=author)
    if follow.exists():
        follow.delete()
    return redirect('blog:profile', username)



def likes_index(request):
    """В шаблон likes_index вывести посты,
    которые оценил пользователь, сделавший запрос"""
    likes = Like.objects.filter(user=request.user)
    # коннект между постом и лайком
    # как из лайков получить список постов
    context = {'likes': likes }
    template = 'blog/likes_index.html'
    return render(request, template, context)


def follow_index():
    """В шаблон follow_index посты авторов, на которых
    подписан текущий пользователь"""
    pass

def follow_list():
    """В шаблон follow_list авторов, на которых
        подписан текущий пользователь"""