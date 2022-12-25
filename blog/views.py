from django.shortcuts import render
from django.db.models import Count

from .models import Article, Category


def index_handler(request):
    last_5_articles = Article.objects.all().order_by('-pub_date')[:5].prefetch_related('categories')

    cat_list = Category.objects.annotate(count=Count('article__id')).order_by('count')[:5]

    context = {
        'last_articles': last_5_articles,
        'menu_categories': cat_list
        }
    return render(request, 'blog/index.html', context)


def about_handler(request):
    context = {}
    return render(request, 'blog/about-us.html', context)


def coming_soon_handler(request):
    context = {}
    return render(request, 'blog/coming-soon.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'blog/contact.html', context)


def single_post_handler(request, slug):
    last_3_articles = Article.objects.all().order_by('-pub_date')[:3]
    context = {
        'last_articles': last_3_articles
        }
    return render(request, 'blog/article.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'blog/robots.txt', context,
                  content_type='text/plain')
