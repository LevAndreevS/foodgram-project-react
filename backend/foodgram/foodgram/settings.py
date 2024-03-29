
import os
import re

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'osnfoshvg89e8395-35+-+-=0-34')

DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'djoser',

    'users.apps.UsersConfig',
    'groceryassistant.apps.GroceryassistantConfig',
    'api.apps.ApiConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'django'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', 5432)
    }
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_backend'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_backend'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF settings

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
}

DJOSER = {
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'api.serializers.MyUserCreateSerializer',
        'user': 'api.serializers.MyUserListSerializer',
        'current_user': 'api.serializers.MyUserListSerializer',
        'set_password': 'api.serializers.UserPasswordSerializer',
    },
    'PERMISSIONS': {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    },
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

AUTH_USER_MODEL = 'users.User'

# Constants
# common
NAME_LENGTH = 200
NUMBER_OF_DISPLAY_DIGITS = 15
# users.models.py
MAX_LENGTH = 150
EMAIL_LENGTH = 254
# groceryassistant.models.py
SLUG_LENGTH = 50
COLOR_LENGTH = 7
# groceryassistant.serializers.py
MIN_AMOUNT_TAG = 1
MIN_AMOUNT_INGREDIENT = 1
TIME_MIN_COOKING = 1
TIME_MAX_COOKING = 600
# groceryassistant.validators.py
REGEX_FOR_USER_LOGIN = re.compile(r'^[\w.@+-]+\Z')
REGEX_FOR_TAG_SLUG = re.compile(r'^[-a-zA-Z0-9_]+$')
FORBIDDEN_LOGIN = 'me'
MIN_AMOUNT = 1
# groceryassistant.management.commands.import_csv.py
SUCCESS_IMPORT = 'Импорт файла ingredients.csv завершен успешно!'
DUPLICATE_INGREDIENTS = 'Такие ингредиенты уже есть!'
ERROR_FIND_FILE = 'Отсутствует файл ingredients в директории backend/data'
PATH = str(BASE_DIR.joinpath('/foodgram/data').resolve()) + '/'
FILENAME = 'ingredients.csv'
# groceryassistant.admin.py
EMPTY = '-пусто-'
