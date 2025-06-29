from django.shortcuts import render
from .models import Post

def get_post_list(request):
    posts = Post.objects.all() # Импорт всех постов из бд и сохранение в переменной
# если заменить all на order_by('created_at'), то будет сортировка по дате создания
# если написать -created_at, то будет сортировка в обратном порядке

    return render(request, 'python/post_list.html', context={'posts': posts})
