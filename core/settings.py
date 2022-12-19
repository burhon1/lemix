from pathlib import Path
import os, sys

# pyton-dotenv
from dotenv import  load_dotenv
load_dotenv('.env')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k%qh!4%iiwyfn)xtmc5qpckb_#zq1k=@tw!%pg(1832#)-p(7z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

# Append module dir
sys.path.append(os.path.join(BASE_DIR, 'apps'))

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*'] # '5.8.248.139','t.lemix.uz','localhost', '127.0.0.1'
DEFAULT_DOMAIN = 'https://{}'.format(ALLOWED_HOSTS[0])
CSRF_TRUSTED_ORIGINS = ['http://5.8.248.139','http://lemix.uz/','https://lemix.uz','https://*.lemix.uz','http://*.lemix.uz','http://lemix.uz','https://lemix.uz','http://*','https://*',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pyclick',
    'rest_framework',
    'paycomuz',
    'user',
    'education',
    'admintion',
    'student',
    'finance',
    'clickuz',
    'django_user_agents',
    'import_export',
]
# bu Click Settings
CLICK_SETTINGS = {
    'service_id': os.getenv("CLICK_SERVICE_ID"),
    'merchant_id': os.getenv("CLICK_MERCHANT_ID"),
    'secret_key': os.getenv("CLICK_SECRET_KEY"),
    'merchant_user_id': os.getenv("CLCIK_MERCHANT_USER_ID"),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    # 'admintion.middleware.page_access.check_user_page_access',
    # 'admintion.middleware.logger.write_logger',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
            'admintion_tags': 'admintion.templatetags.custom_tags',
            'education_tags': 'education.templatetags.education_tags',
            'user_tags': 'user.templatetags.user_tags',
            }

        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
AUTH_USER_MODEL  = 'user.CustomUser'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lemix',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }

}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PAYCOM_SETTINGS = {
    "KASSA_ID": "635795929fd41bc3daf5019c",
    "TOKEN": "635795929fd41bc3daf5019c",  # token
    "SECRET_KEY": "HqEBBzMOwmCJ5G#pju9F75QMCnua2H1iCH?d",  # password
    "ACCOUNTS": {
        "KEY": "Lemix_kassa"
    }
}

CLICK_SETTINGS = {
    'service_id':'25807',
    'merchant_id':'18147',
    'secret_key':'HHPm2yaWiIwb'
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (str(BASE_DIR.joinpath('static')),)
# STATIC_ROOT = str(BASE_DIR.joinpath('static'))
MEDIA_URL = '/media/uploads/'
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

LOGIN_URL = '/user/login/'