from utils.signals.slug import slug_with_date
from .models import Blog

# Criar slug automático
slug_with_date(sender=None, instance=Blog)
