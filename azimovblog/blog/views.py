from django.shortcuts import render, get_object_or_404

from .models import Post, Category


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


def category_info():
    pass


def all_category(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    template = 'blog/all_categories.html'
    return render(request, template, context)
