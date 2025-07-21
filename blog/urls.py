from django.urls import path
from .views import get_post_list, get_post_detail, create_post, update_post, delete_post   # импорт вьюшки

urlpatterns = [
    path('posts/', get_post_list, name='post_list'),
    path('posts/<int:id>/', get_post_detail, name='get_post_detail'),
    path('posts/add', create_post, name='new_post'),
    path('posts/<int:id>/edit/', update_post, name='edit_post'),
    path('posts/<int:id>/delete/', delete_post, name='remove_post')
]