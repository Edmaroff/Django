# coding=utf-8

from django.db import models
from django.urls import reverse


class Book(models.Model):
    name = models.CharField(u'Название', max_length=64)
    author = models.CharField(u'Автор', max_length=64)
    pub_date = models.DateField(u'Дата публикации')

    def __str__(self):
        return self.name + " " + self.author

    def get_absolute_url(self):
        return reverse('composition', kwargs={'date': self.pub_date})
