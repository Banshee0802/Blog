from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from unidecode import unidecode

def get_post_list(request):
    posts = Post.objects.filter(status='published') # Импорт всех постов из бд и сохранение в переменной
# если заменить all на order_by('created_at'), то будет сортировка по дате создания
# если написать -created_at, то будет сортировка в обратном порядке
    return render(request, 'python/post_list.html', context={'posts': posts})


def get_post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    context = {'post': post}

    return render(request, 'python/post_detail.html', context)

@login_required
def create_post(request):
    title = "Создать пост"
    submit_button_text = 'Создать'

    if request.method == 'GET':
        form = PostForm()

        return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            new_tags = form.cleaned_data['new_tags']
            if new_tags:
                for tag_name in new_tags.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        # Создаем или получаем тег
                        tag, created = Tag.objects.get_or_create(
                            name=tag_name,
                            defaults={'slug': slugify(unidecode(tag_name))}
                        )
                        post.tags.add(tag)
            form.save_m2m()

            return redirect('get_post_detail', post_slug=post.slug)
        else:
            return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})
        

def update_post(request, post_slug):
    title = "Редактировать пост"
    submit_button_text = 'Обновить'
    post = get_object_or_404(Post, slug=post_slug)

    initial_tags = ', '.join([tag.name for tag in post.tags.all()])

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            updated_post = form.save()

            updated_post.tags.clear()

            tags_input = form.cleaned_data['tags_input']
            if tags_input:
                for tag_name in tags_input.split(','):
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(
                            name=tag_name,
                            defaults={'slug': slugify(unidecode(tag_name))}
                        )
                        updated_post.tags.add(tag)
        
            return redirect('get_post_detail', post_slug=updated_post.slug)
        else:
            return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})

    form = PostForm(instance=post, initial={'tags_input': initial_tags})
    
    return render(request, 'python/post_form.html', context={'form': form, 'title': title, 'submit_button_text': submit_button_text})


def delete_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)

    if request.method == 'POST':
        post.delete()

        return redirect('post_list')
    
    return render(request, 'python/confirm_post_delete.html', {'post': post})


def main_page_view(request):
    return render(request, 'python/main_page.html')


def get_posts_by_category(request, category_slug):
    """Показывает посты определенной категории"""
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, status='published')
    
    return render(request, 'python/posts_by_category.html', {
        'category': category,
        'posts': posts
    })

def get_category_list(request):
    """Показывает список всех категорий"""
    categories = Category.objects.all()
    return render(request, 'python/category_list.html', {
        'categories': categories
    })


def get_posts_by_tag(request, tag_slug):
    """Показывает посты определенного тега"""
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    return render(request, 'blog/posts_by_tag.html', {
        'tag': tag,
        'posts': posts
    })

def get_tag_list(request):
    """Показывает список всех тегов"""
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {
        'tags': tags
    })