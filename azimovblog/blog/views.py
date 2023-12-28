from django.shortcuts import render, get_object_or_404

from .models import Post, Category, User, Profile, Comment, Like, Follow


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
    context = {
        'post': post
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
    prof = user.profile
    posts = user.post.all()
    context = {
        'user': user,
        'profile': prof,
        'posts': posts,

    }
    template = 'blog/profile.html'
    return render(request, template, context)
