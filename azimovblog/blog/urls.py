from django.urls import path

from .views import (index, post_info, category_info, all_category, profile,
                    search, add_like, del_like, add_sub, del_sub, PostCreate)

from django.contrib.auth.decorators import login_required

app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
    path('blog/<int:pk>/', post_info, name='post_info'),
    path('category/', all_category, name='all_category'),
    path('category/<slug>/', category_info, name='category_info'),
    path('profile/<str:username>/', profile, name='profile'),
    path('search/', search, name='search'),
    path('blog/<int:pk>/add_like/', add_like, name='add_like'),
    path('blog/<int:pk>/del_like/', del_like, name='del_like'),

    path('profile/<str:username>/follow/', add_sub, name='follow'),
    path('profile/<str:username>/unfollow/', del_sub, name='unfollow'),

    path('create_post/', login_required(PostCreate.as_view()), name='create'),

]
