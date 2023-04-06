from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lemixprod',
        'USER': 'lemixproduser', #  djangouser  postgres
        'PASSWORD': 'Hh*-u9^.nR{<6qAr',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }

}

STATIC_ROOT = str(BASE_DIR.joinpath('static'))