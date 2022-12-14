from django.db import models

from tinymce.models import HTMLField

from string import punctuation

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    in_menu = models.BooleanField(default=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Author(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars')
    bio = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Article(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content_words_count = models.IntegerField(null=True, blank=True)
    content = HTMLField()
    short_description = HTMLField()
    main_image = models.ImageField(upload_to='images')
    pub_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def count_unique_words(self):
        text = self.content.replace('<p>', "").replace('</p>', "")
        for symbol in punctuation:
            text.replace(symbol, '')
        words = text.split()
        return len(set(words))


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    website = models.CharField(max_length=255)
    comment = HTMLField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:20]


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscription_date = models.DateTimeField(auto_now_add=True)
    unsubscription_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.name
