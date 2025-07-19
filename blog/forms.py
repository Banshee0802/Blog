from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Максимальная длина 200 символов',
            })
        }
        labels = {
            'title': 'Заголовок поста',
            'content': 'Текст поста'
        }
    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        
        if len(title) < 5:
            raise forms.ValidationError('Заголовок не должен быть короче 5 символов')

        return title



# class PostForm(forms.Form):
#     title = forms.CharField(
#         max_length=200,
#         label='Заголовок поста:',
#         required=False,
#         widget=forms.TextInput(attrs={
#             'placeholder': 'Максимальная длина 200 символов',
#         })
#     )
#     content = forms.CharField(
#         label='Текст поста:',
#         widget=forms.Textarea(attrs={
#             'rows': 3
#         })
#     )

#     def clean_title(self):
#         title = self.cleaned_data['title'].strip()
        
#         if len(title) < 5:
#             raise forms.ValidationError('Заголовок не должен быть короче 5 символов')

#         return title