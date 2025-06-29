from django.urls import path
from .views import get_post_list, get_post_detail    # импорт вьюшки

urlpatterns = [
    path('posts/', get_post_list, name='post_list'),
    path('posts/<int:id>/', get_post_detail, name='get_post_detail')
]