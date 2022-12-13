# -*- coding: utf-8 -*-
from datetime import datetime

from slugify import slugify
from requests_html import HTMLSession
'''
Многопоточность у меня не заработала. При отправке запросов (session.get)
 в несколько потоков. Приложениие просто завершалось без вывода и без вызова
 каких либо ошибок.
'''
# from concurrent.futures import ThreadPoolExecutor

from blog.models import Article, Author, Category


def get_author_meta(author_name, url):  # Получаем изображение и описание автора
    with HTMLSession() as session:
        response = session.get(url)
        response.html.render(timeout=200)
        bio = response.html.xpath('//div[@class="author-description"]')[0].text
        image_url = response.html.xpath('//img[contains(@class, "avatar")]/@src')[0]
        image_name = slugify(author_name)
        image_type = image_url.split('.')[-1]
        image_path = f'/avatars/{image_name}.{image_type}'
        with open(f'media/{image_path}', 'wb') as f:
            with HTMLSession() as session:
                response = session.get(image_url)
                f.write(response.content)
    return image_path, bio


# Парсер статей
def crawl_one(url):
    print(f'Запустили crawl_one c URL {url}')

    with HTMLSession() as session:
        response = session.get(url)
        response.html.render(timeout=200)  # На сайте используется Lazy load

        name = response.html.xpath('//h1[contains(@class, "post-title")]')[0].text
        content = response.html.xpath('//div[@class="post-content entry-content"]/p')
        try:
            image_url = response.html.xpath('//img[contains(@class, "alignnone size-full")]/@src')[0]
        except IndexError:
            image_url = None
        pub_date = response.html.xpath('//div[contains(@class, "post-date")]/time/@datetime')[0]
        my_content = ''
        short_description = ''
        for element in content:
            my_content += f'<{element.tag}>' + element.text + f'</{element.tag}>'
            if len(short_description) <= 200:
                short_description += element.text + ' '
        if image_url is not None:
            image_name = slugify(name)
            image_type = image_url.split('.')[-1]
            image_path = f'images/{image_name}.{image_type}'
            with open(f'media/{image_path}', 'wb') as f:
                with HTMLSession() as session:
                    response = session.get(image_url)
                    f.write(response.content)
        else:
            image_path = None

        pub_date = datetime.fromisoformat(pub_date)
        author_name = response.html.xpath('//strong[@class="author vcard"]')[0].text
        author_url = response.html.xpath('//strong[@class="author vcard"]/a/@href')[0]
        author_avatar, author_bio = get_author_meta(author_name, author_url)
        cats = response.html.xpath('//ul[@class="post-tags"]/li')

    article_categories = []
    for cat in cats:
        article_categories.append(
            {
                'name': cat.text.strip(),
                'slug': slugify(cat.text)
                }
            )
    if len(article_categories) == 0:
        article_categories = None

    author = {
        'name': author_name,
        'avatar': author_avatar,
        'bio': author_bio,
        }

    article = {
        'name': name,
        'slug': slugify(name),
        'content': my_content,
        'short_description': short_description.strip(),
        'main_image': image_path,
        'pub_date': pub_date,
        }
    author, created = Author.objects.get_or_create(**author)
    article['author'] = author
    print('Создали экземпляр класса Автор')

    if article_categories is not None:
        categories = []
        for category in article_categories:
            cat, created = Category.objects.get_or_create(**category)
            categories.append(cat)
        article['categories'] = categories

    print('Создали экземпляр класса Категория')
    print(f'Статья {article.name} готова для записи в базу данных')

    article, created = Article.objects.get_or_create(**article)

    print('Статья {article.name} записана в базу данных')


def get_link_collect():
    base_url = 'https://zozhnik.ru'
    links_collect = []

    with HTMLSession() as session:
        for i in range(1, 500):
            response = session.get(f'{base_url}/page/{i}/')
            response.html.render(timeout=200)  # На сайте используется Lazy load
            links = response.html.xpath('//h1[@class="post-title entry-title"]/a/@href')
            if len(links) != 0:
                for item in links:
                    links_collect.append(item)
            else:
                break
    return links_collect


def run():
    links_collect = get_link_collect()
    print('Закончили собирать ссылки')

    for link in links_collect:
        crawl_one(link)

    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.map(crawl_one, links_collect)
