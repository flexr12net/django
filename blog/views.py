from django.shortcuts import render


def index_hendler(request):
    context = {}
    return render(request, 'blog/index.html', context)


def about_hendler(request):
    context = {}
    return render(request, 'blog/about-us.html', context)


def coming_soon_hendler(request):
    context = {}
    return render(request, 'blog/coming-soon.html', context)


def contact_hendler(request):
    context = {}
    return render(request, 'blog/contact.html', context)


def single_post_hendler(request):
    context = {}
    return render(request, 'blog/single-post.html', context)


def robots_hendler(request):
    context = {}
    return render(request, 'blog/robots.txt', context,
                  content_type='text/plain')
