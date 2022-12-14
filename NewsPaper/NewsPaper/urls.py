from django.contrib import admin
from django.urls import path, include

from newsportal.views import PostsList, PostDetail, PostSearch, subscribe
from sign.views import AccountView, set_user_group_to_common

# from newsportal.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('newsportal.urls')),
    path('articles/', include('newsportal.urls_articles')),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('', PostsList.as_view()),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('account/', AccountView.as_view()),
    path('common/', set_user_group_to_common),
    path('subscribe/', subscribe),
    #path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    #path('hello/', IndexView.as_view())
]
