from django.urls import path

from .views import index, post_info


app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
    path('blog/<int:pk>/', post_info, name='post_info'),

]

"""
127.0.0.1:8000/blog/1/
127.0.0.1:8000/blog/2/
127.0.0.1:8000/blog/3/
127.0.0.1:8000/blog/steamdeck/
127.0.0.1:8000/blog/5/
127.0.0.1:8000/blog/6/
127.0.0.1:8000/blog/7/
127.0.0.1:8000/blog/8/
127.0.0.1:8000/blog/9/
127.0.0.1:8000/blog/10/
"""