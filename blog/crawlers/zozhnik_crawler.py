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
        try:
            bio = response.html.xpath('//div[@class="author-description"]')[0].text
        except:
            bio = ''
        image_url = response.html.xpath('//img[contains(@class, "avatar")]/@src')[1]
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
        print(f'Отправляем запрос на адрес {url}')
        response = session.get(url)
        print(f'Запрос отправлен. Запускаем ренедер {url}')
        response.html.render(timeout=200)  # На сайте используется Lazy load
        print(f'Рендер {url} Завершен.')
        name = response.html.xpath('//h1[contains(@class, "post-title")]')[0].text
        print(f'Извлечено название статьи. {name} Тип {type(name)}')
        content = response.html.xpath('//div[@class="post-content entry-content"]/p')
        print(f'Получен контент Тип {type(content)}')
        try:
            image_url = response.html.xpath('//img[contains(@class, "alignnone size-full")]/@src')[0]
            print(f'Получен URL изображения. URL {image_url} Размер {len(image_url)}')
        except IndexError:
            image_url = None
            print('Изображения нет')
        pub_date = response.html.xpath('//div[contains(@class, "post-date")]/time/@datetime')[0]
        cats = response.html.xpath('//ul[@class="post-tags"]/li')
        print(f' !!!!!!! {cats}')
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

#  Получаем Автора
        author = {}
        try:
            author['name'] = response.html.xpath('//strong[@class="author vcard"]')[0].text
            author_url = response.html.xpath('//strong[@class="author vcard"]/a/@href')[0]
            author['avatar'], author['bio'] = get_author_meta(author['name'], author_url)

        except IndexError:
            author = {
                    'name': 'unknown',
                    'avatar': 'default_avatar',
                    'bio': 'default_bio',
                    }

# Получаем Категории
    article_categories = []
    for cat in cats:
        article_categories.append(
            {
                'name': cat.text.strip(),
                'slug': slugify(cat.text)
                }
            )
    if len(article_categories) == 0:
        print('Категории пустые')
        article_categories.append(
            {
                'name': 'no category',
                'slug': slugify('no category')
                }
            )

    article = {
        'name': name,
        'slug': slugify(name),
        'content': my_content,
        'short_description': short_description.strip(),
        'main_image': image_path,
        'pub_date': pub_date,
        }
    if author is not None:
        author, created = Author.objects.get_or_create(**author)
        article['author'] = author
    print('Создали экземпляр класса Автор')

    article, created = Article.objects.get_or_create(**article)

    print('Категории не пустые')
    print(f'Получено {len(article_categories)} категорий')
    for category in article_categories:
        print(f'Обрабатываем категорию {category}')
        cat, created = Category.objects.get_or_create(**category)
        print('Создали экземпляр класса Категория')
        article.categories.add(cat)
    print('Статья {article.name} записана в базу данных')

def get_link_collect():
    base_url = 'https://zozhnik.ru'
    links_collect = []
    print('Собираем ссылки. Это долго.')

    with HTMLSession() as session:
        for i in range(1, 2):
            print(f'Делаем запрос на станицу {base_url}/page/{i}/')
            response = session.get(f'{base_url}/page/{i}/')
            print('Запрос выполнен. Начинаем Рендер')
            response.html.render(timeout=200)  # На сайте используется Lazy load
            print('Рендер выполнен')
            links = response.html.xpath('//h1[@class="post-title entry-title"]/a/@href')
            print(f'Получены ссылки {links} в количестве {len(links)} шт')
            if len(links) != 0:
                for item in links:
                    links_collect.append(item)
            else:
                break
    return links_collect


def run():
    links_collect = get_link_collect()
    print('Закончили собирать ссылки')
    print(f'Нашли вот что {links_collect}')

    for link in links_collect:
        print(f'Парсим страницу {link}')
        crawl_one(link)
        print(f'Парсинг страницы {link} закончен.')

    # with ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.map(crawl_one, links_collect)
