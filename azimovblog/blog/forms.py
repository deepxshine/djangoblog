from django.forms import ModelForm

from .models import Post


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'image']
        help_texts = {
            'category': 'Выберете из списка',
            'image': 'Загрузите картинку'
        }

