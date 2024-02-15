from django.forms import ModelForm

from .models import Post, Comment


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'image']
        help_texts = {
            'category': 'Выберете из списка',
            'image': 'Загрузите картинку'
        }


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']
        help_texts = {
            'text': 'Напишите комментарий',
            'image': 'Загрузить картинку'
        }