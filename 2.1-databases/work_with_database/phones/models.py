from django.db import models
from slugify import slugify


class Phone(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=100)

    def save(self, args, **kwargs):
        self.slug = slugify(self.name)
        super(Phone, self).save(args, **kwargs)
