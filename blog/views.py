from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from unidecode import unidecode

from .models import Post, Category, Tag
from .forms import PostForm

class PostListView(ListView):
    model = Post
    template_name = 'python/post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(status='published')

class PostDetailView(DetailView):
    model = Post
    template_name = 'python/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'python/post_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Создать пост"
        context['submit_button_text'] = 'Создать'
        return context
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        
        # Сохраняем пост (slug автоматически сгенерируется в методе save() модели)
        post.save()
        
        # Обработка тегов
        tags_input = form.cleaned_data.get('tags_input', '')
        if tags_input:
            for tag_name in tags_input.split(','):
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(unidecode(tag_name))}
                    )
                    post.tags.add(tag)
        
        # Редирект на детали поста
        return redirect('get_post_detail', post_slug=post.slug)
    
    def get_success_url(self):
        return reverse_lazy('get_post_detail', kwargs={'post_slug': self.object.slug})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'python/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактировать пост"
        context['submit_button_text'] = 'Обновить'
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        initial['tags_input'] = ', '.join([tag.name for tag in self.object.tags.all()])
        return initial
    
    def form_valid(self, form):
        # Очищаем старые теги
        self.object.tags.clear()
        
        # Обработка новых тегов
        tags_input = form.cleaned_data.get('tags_input', '')
        if tags_input:
            for tag_name in tags_input.split(','):
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(unidecode(tag_name))}
                    )
                    self.object.tags.add(tag)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('get_post_detail', kwargs={'post_slug': self.object.slug})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'python/confirm_post_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class MainPageView(TemplateView):
    template_name = 'python/main_page.html'

class PostsByCategoryView(ListView):
    template_name = 'python/posts_by_category.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Post.objects.filter(category=self.category, status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'python/category_list.html'
    context_object_name = 'categories'

class PostsByTagView(ListView):
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags=self.tag, status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class TagListView(ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'