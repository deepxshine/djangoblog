from django.contrib import admin

from .models import Post, Category



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'category',
        'pubdate'
    )
    search_fields = ('title', 'category', 'author',)
    list_filter = ('pubdate', 'category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'age_limit',
        'post_count',
    )
    list_filter = ('age_limit',)

    def post_count(self, obj):
        return obj.posts.count()
