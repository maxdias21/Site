from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime


# Criar slug automático
@receiver(post_save, sender=None)
def slug_with_date(sender, instance, *args, **kwargs):
    if instance.__class__.__name__ == 'LogEntry':
        return

    if(sender.__class__.__name__):
        return

    if kwargs.get('created'):
        date = datetime.strptime(
            f'{instance.created_at.day}-{instance.created_at.month}-{instance.created_at.year}'
            f'-{instance.created_at.microsecond}',
            '%d-%m-%Y-%f')

        instance.slug = slugify(f'{instance.title}-{date}')
        instance.save()
        return

    return
