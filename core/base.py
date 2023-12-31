from pathlib import Path
import os, sys

# pyton-dotenv
# from dotenv import  load_dotenv
# load_dotenv('.env')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent # local
# BASE_DIR =  # deploy

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k%qh!4%iiwyfn)xtmc5qpckb_#zq1k=@tw!%pg(1832#)-p(7z'

# Append module dir
sys.path.append(os.path.join(BASE_DIR, 'apps'))

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['t.lemix.uz','*'] # '5.8.248.139','t.lemix.uz','localhost', '127.0.0.1'
DEFAULT_DOMAIN = 'https://{}'.format(ALLOWED_HOSTS[0])
CSRF_TRUSTED_ORIGINS = ['http://5.8.248.139','http://lemix.uz/','https://lemix.uz','https://*.lemix.uz','http://*.lemix.uz','http://lemix.uz','https://lemix.uz','http://*','https://*', 'https://*.eu.ngrok.io']

# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'user',
    'education',
    'admintion',
    'student',
    'finance',
    'django_user_agents',
    'import_export',
    'sms',
    'django_cleanup.apps.CleanupConfig',
    'pyclick',
    'manages'

]
# bu Click Settings
CLICK_SETTINGS = {
    'service_id': '25807',
    'merchant_id': '18147',
    'secret_key': 'HHPm2yaWiIwb',
    'merchant_user_id': '29268',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
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
    'admintion.middlewares.FirstMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'admintion.admintion_processors.branch_list',
                'admintion.admintion_processors.user_groups'
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
ESKIZ_EMAIL = {
    'email':'programmer2705@gmail.com',
    'password': 'TGFbHxerK7osSYsRpK11LLDt1LX5obYvqOpktufP'
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

MEDIA_URL = '/media/uploads/'
MEDIA_ROOT = str(BASE_DIR.joinpath('media'))

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

LOGIN_URL = '/user/login/'