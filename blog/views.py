from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


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
        form = PostForm()

        return render(request, 'python/post_add.html', context={'form': form})
    
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = Post.objects.create(
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content']
            )

            return redirect('get_post_detail', id=post.id)
        else:
            return redirect('post_list')