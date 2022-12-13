# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from blog.crawlers.zozhnik_crawler import run


class Command(BaseCommand):
    help = 'Run zozhnik.ru crawler'

    def handle(self, *args, **options):
        run()
