from .environment import BASE_DIR


# URL
STATIC_URL = '/static/'

# Local de salvamento dos arquivos estáticos depois que fizer deploy
STATIC_ROOT = BASE_DIR / 'static/'

# Local de salvamento dos arquivos estáticos em modo de desenvolvimento
STATICFILES_DIRS = [
    BASE_DIR / 'global_statics',
]

# Url
MEDIA_URL = '/media/'

# Local de salvamento
MEDIA_ROOT = BASE_DIR / 'media/'
