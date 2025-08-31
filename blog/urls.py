from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    MainPageView, PostsByCategoryView, CategoryListView, PostsByTagView, TagListView
)

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/add/', PostCreateView.as_view(), name='new_post'),
    path('posts/<slug:post_slug>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('posts/<slug:post_slug>/delete/', PostDeleteView.as_view(), name='remove_post'),
    path('posts/<slug:post_slug>/', PostDetailView.as_view(), name='get_post_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', PostsByCategoryView.as_view(), name='posts_by_category'),
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tag/<slug:tag_slug>/', PostsByTagView.as_view(), name='posts_by_tag'),
]
