from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, )

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        exists = Tag.objects.filter(slug=self.name).first()

        if exists:
            raise ValidationError({'name': 'Essa tag já existe'})

        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
