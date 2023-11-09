from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    LIMITS = [
        ('0+', '0+'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('16+', '16+'),
        ('18+', '18+'),
    ]

    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    age_limit = models.CharField(max_length=3, choices=LIMITS,
                                 verbose_name='Возрастое ограничение')
    image = models.ImageField(upload_to='category', verbose_name='Картинка', blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    image = models.ImageField(upload_to='post/', verbose_name='Картинка', blank=True)
    pubdate = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата публикации')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория', related_name='posts')


    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


