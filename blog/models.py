from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True) # автоматический счет времени

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        db_table = 'blog_posts'

    def __str__(self):   # функция для отображения названия поста
        return self.title
    

