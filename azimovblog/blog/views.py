from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
# Create your views here.

from .models import Post


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
