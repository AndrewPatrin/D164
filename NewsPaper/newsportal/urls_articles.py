from django.urls import path
# Импортируем созданное нами представление
from .views import ArticlesList, ArticleDetail, ArticleSearch, ArticleCreate, ArticleEdit, ArticleDelete


urlpatterns = [
    path('', ArticlesList.as_view(), name='articles_list'),
    path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path("search/", ArticleSearch.as_view(), name='article_search'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

]
