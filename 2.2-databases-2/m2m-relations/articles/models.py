from django.db import models
from django.db.models import F


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=70, unique=True, verbose_name='Название тега')
    articles = models.ManyToManyField(Article, related_name='tags', through='Scope')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        # ordering = ['name']


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Название тега', related_name='scopes_tag')
    is_main = models.BooleanField(default=False, verbose_name='Основной тег?')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        ordering = ['-is_main', 'tag__name']