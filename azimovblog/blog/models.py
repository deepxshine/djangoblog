from django.contrib.auth import get_user_model
from django.db import models

from .core import kirillic_slugify

User = get_user_model()


class Profile(models.Model):
    """Аватар, описание, дата рождения"""
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    image = models.ImageField(upload_to='avatars/', blank=True,
                              verbose_name='Аватарка')
    birthday = models.DateField()

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return str(self.user)


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
    image = models.ImageField(upload_to='category', verbose_name='Картинка',
                              blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = kirillic_slugify(self.title)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор', related_name='post')
    image = models.ImageField(upload_to='post/', verbose_name='Картинка',
                              blank=True)
    pubdate = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата публикации')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 related_name='posts')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pubdate']

    def __str__(self):
        return self.title


class Like(models.Model):
    """Лайки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='liker')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='liked_post')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='flwr',
                                 db_comment='Тот на кого подписываются')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='flwg',
                                  db_comment='Тот кто подписывается')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Comment(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name='comm_author',
                                       verbose_name='Автор')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comm_post', verbose_name='Пост')
    text = models.CharField(max_length=512, verbose_name="Текст комментария")
    image = models.ImageField(upload_to='comments', verbose_name='Картинка',
                              blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
