from django.urls import path
from blogs.apps import BlogsConfig
from blogs.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdatelView, ArticleDeleteView

app_name = BlogsConfig.name
urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('list/', ArticleListView.as_view(), name='list'),
    path('view/<int:pk>/', ArticleDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', ArticleUpdatelView.as_view(), name='edit'),
    path('delete/<int:pk>/', ArticleDeleteView.as_view(), name='delete')
]
