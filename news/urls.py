from . import views
from django.urls import path

urlpatterns = [
    path('', views.coming_soon, name='coming_soon'),
    path("news/<int:article_id>/", views.article_view, name="article_view"),
    path("news/", views.news_view, name="index"),
    path("news/create/", views.create_article, name="create_article")
]
