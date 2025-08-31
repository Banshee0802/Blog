from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label='Теги',
        help_text='Введите теги через запятую (например: цветы, сад, декор)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'теги через запятую'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Максимальная длина 200 символов',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'title': 'Заголовок поста',
            'content': 'Текст поста',
            'image': 'Картинка поста',
            'category': 'Категория поста',
            'status': 'Статус'
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        
        if len(title) < 5:
            raise forms.ValidationError('Заголовок не должен быть короче 5 символов')

        return title
