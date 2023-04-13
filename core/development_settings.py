from .base import *
from django.core.exceptions import ImproperlyConfigured

LLOWED_HOSTS = ['localhost']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

def get_env_value(env_variable):
    try:
        print(os.environ['NAME'])
        return os.environ[env_variable]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(env_variable)
        raise ImproperlyConfigured(error_msg)

# SECRET_KEY = get_env_value('SECRET_KEY')
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
        'HOST': 't.lemix.uz',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': get_env_value('DATABASE_NAME'),
#         'USER': get_env_value('DATABASE_USER'),
#         'PASSWORD':get_env_value('DATABASE_PASSWORD'),
#         'HOST': get_env_value('DATABASE_HOST'),
#         'PORT': int(get_env_value('DATABASE_PORT')),
#     }
# }

STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)