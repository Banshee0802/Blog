from django.urls import path
from .views import home_view    # импорт вьюшки

urlpatterns = [
    path('', home_view)
]