from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from .views import SignUp

app_name = 'user'

urlpatterns = [
    path('logout/', LogoutView.as_view(template_name='user/logged_out.html'),
         name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='user/login.html'),
         name="login")
]
