# -*- coding: utf-8 -*-
from django.db.models import Count

from .models import Category


def menu_categories(request):
    cat_list = Category.objects.annotate(
        count=Count('article__id')).order_by('-count')[:5]
    return {'menu_categories': cat_list}
