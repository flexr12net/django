from django.shortcuts import render
from django.db.models import Count

from .models import Article, Category


def index_handler(request,):
    last_5_articles = Article.objects.all().order_by(
        '-pub_date')[:5].prefetch_related('categories')

    context = {
        'last_articles': last_5_articles,
        }
    return render(request, 'blog/index.html', context)


def blog_handler(request, **kwargs):
    cat_slug = kwargs.get('cat_slug')
    if cat_slug:
        category = Category.objects.get(slug=cat_slug)
        last_articles = Article.objects.filter(categories__slug=cat_slug).order_by(
            '-pub_date')[:10].prefetch_related('categories')
    else:
        last_articles = Article.objects.all().order_by(
            '-pub_date')[:10].prefetch_related('categories')
        category = None
    context = {
        'last_articles': last_articles,
        'category': category
        }
    return render(request, 'blog/blog.html', context)


def about_handler(request):
    context = {}
    return render(request, 'blog/about-us.html', context)


def coming_soon_handler(request):
    context = {}
    return render(request, 'blog/coming-soon.html', context)


def contact_handler(request):
    context = {}
    return render(request, 'blog/contact.html', context)


def single_post_handler(request, post_slug):
    article = Article.objects.get(slug=post_slug)
    last_3_articles = Article.objects.all().order_by('-pub_date')[:3]
    context = {
        'last_articles': last_3_articles,
        'article': article
        }
    return render(request, 'blog/article.html', context)


def robots_handler(request):
    context = {}
    return render(request, 'blog/robots.txt', context,
                  content_type='text/plain')
