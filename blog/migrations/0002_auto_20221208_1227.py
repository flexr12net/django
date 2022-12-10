# Generated by Django 3.2.5 on 2022-12-08 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='article',
            name='main_image',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(upload_to='images'),
        ),
    ]
