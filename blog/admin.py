from django.contrib import admin
from django.utils.html import format_html
# Register your models here.

from .models import Article, Author, Category, Newsletter, Comment


def count_words(modeladmin, request, queryset):
    for object in queryset:
        text = object.content.replace('<p>', "").replace('</p>', "")
        words = text.split()
        object.content_words_count = len(words)
        object.save()


count_words.short_description = 'Count words in article.'


class CommentArticleInLine(admin.TabularInline):
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date', 'author',
                    'content_words_count', 'count_unique_words')
    list_filter = ('author', 'pub_date', 'categories')
    search_fields = ('name', 'author__name')
    actions = [count_words]
    inlines = (CommentArticleInLine, )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_menu', 'order', 'articles_count')
    list_filter = ('in_menu',)
    search_fields = ('name',)
    list_editable = ('order',)
    readonly_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('article_set')

    def articles_count(self, object):
        return object.article_set.all().count()


class AuthorArticleInLine(admin.TabularInline):
    model = Article
    exclude = ('content', 'short_description')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (AuthorArticleInLine, )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Newsletter)
admin.site.register(Comment)
