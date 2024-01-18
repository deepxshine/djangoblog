from django.urls import path

from .views import index, post_info, category_info, all_category, profile, search


app_name = 'blog'


urlpatterns = [
    path('', index, name='index'),
    path('blog/<int:pk>/', post_info, name='post_info'),
    path('category/', all_category, name='all_category'),
    path('category/<slug>/', category_info, name='category_info'),
    path('profile/<str:username>/', profile, name='profile'),
    path('search/', search, name='search'),
]
