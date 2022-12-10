from django.contrib import admin

# Register your models here.

from .models import Article, Author, Category, Newsletter, Comment

admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Newsletter)
admin.site.register(Comment)
