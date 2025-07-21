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
    title = "Создать пост"
    submit_button_text = 'Создать'

    if request.method == 'GET':
        form = PostForm()

        return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
    
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save()

            return redirect('get_post_detail', id=post.id)
        else:
            return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
        

def update_post(request, id):
    title = "Редактировать пост"
    submit_button_text = 'Обновить'
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            updated_post = form.save()

            return redirect('get_post_detail', id=updated_post.id)
        else:
            return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})

    form = PostForm(instance=post)
    
    return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})


def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        post.delete()

        return redirect('post_list')
    
    return render(request, 'python/confirm_post_delete.html', {'post': post})