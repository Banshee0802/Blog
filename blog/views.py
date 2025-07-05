from django.shortcuts import render, get_object_or_404, redirect
from .models import Post


def get_post_list(request):
    posts = Post.objects.all() # Импорт всех постов из бд и сохранение в переменной
# если заменить all на order_by('created_at'), то будет сортировка по дате создания
# если написать -created_at, то будет сортировка в обратном порядке
    return render(request, 'python/post_list.html', context={'posts': posts})


def get_post_detail(request, id):
    # post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id)

    context = {'post': post}

    return render(request, 'python/post_detail.html', context)


def create_post(request):
    if request.method == 'GET':
        return render(request, 'python/post_add.html')
    
    if request.method == 'POST':

        post = Post.objects.create(title=request.POST.get('title'), content=request.POST.get('content'))

        return redirect('get_post_detail', id=post.id)
    
