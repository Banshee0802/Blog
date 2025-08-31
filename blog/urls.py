from django.urls import path
from .views import main_page_view, get_post_list, get_post_detail, create_post, update_post, delete_post, get_posts_by_category, get_category_list, get_tag_list, get_posts_by_tag   # импорт вьюшки


urlpatterns = [
    path('', main_page_view, name='main_page'),
    path('posts/', get_post_list, name='post_list'),
    path('posts/<slug:post_slug>/', get_post_detail, name='get_post_detail'),
    path('posts/add', create_post, name='new_post'),
    path('posts/<slug:post_slug>/edit/', update_post, name='edit_post'),
    path('posts/<slug:post_slug>/delete/', delete_post, name='remove_post'),
    path('categories/', get_category_list, name='category_list'),  # список категорий
    path('category/<slug:category_slug>/', get_posts_by_category, name='posts_by_category'),
    path('tags/', get_tag_list, name='tag_list'),  # список тегов
    path('tag/<slug:tag_slug>/', get_posts_by_tag, name='posts_by_tag'),
]