from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsCreate, NewsEdit, NewsSearch, NewsDelete


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path("search/", NewsSearch.as_view(), name='news_search'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete')
]
