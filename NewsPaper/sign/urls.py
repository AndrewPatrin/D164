from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView

from .views import BaseRegisterView, set_user_group_author, activate

urlpatterns = [
    path('', RedirectView.as_view(url='/sign/login/')),
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('promote/', set_user_group_author, name='set_user_group_author'),
    path('activate/<uidb64>/<token>', activate, name='activate')

]
