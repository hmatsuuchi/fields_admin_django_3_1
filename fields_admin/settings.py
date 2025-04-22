import os
from pathlib import Path
import environ # environment variables
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# initializes environment variables
env = environ.Env(DEBUG=(bool, False))
# dev.env - Development
# prod.env - Production
environ.Env.read_env('./fields_admin/dev.env')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    'corsheaders', # cors headers
    'authentication', # Authentication App
    'students', # Students App
    'schedule', # Schedule App
    'attendance', # Attendance App
    'user_profiles', # User Profiles App
    'journal', # Journal App
    'dashboard', # Dashboard App
    'game', # Game App
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # rest framework
    'rest_framework_simplejwt', # simple jwt
    'rest_framework_simplejwt.token_blacklist', # jwt token blacklist
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # cors headers
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', # use custom csrf middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fields_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fields_admin.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    },
}

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

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'authentication.customAuthentication.CustomAuthentication',
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    "LOGOUT_TOKEN_LIFETIME": timedelta(days=15),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    # access cookie settings
    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_SECURE': True,
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': env('AUTH_COOKIE_SAMESITE'),
    'AUTH_COOKIE_TRUSTED_ORIGINS': env('AUTH_COOKIE_TRUSTED_ORIGINS').split(','),

    # refresh cookie settings
    'REFRESH_COOKIE': 'refresh_token',
    'REFRESH_COOKIE_SECURE': True,
    'REFRESH_COOKIE_HTTP_ONLY': True,
    'REFRESH_COOKIE_PATH': '/api/token/refresh/',
    'REFRESH_COOKIE_SAMESITE': env('REFRESH_COOKIE_SAMESITE'),
    'REFRESH_COOKIE_TRUSTED_ORIGINS': env('REFRESH_COOKIE_TRUSTED_ORIGINS').split(','),

    # logout cookie settings
    'LOGOUT_COOKIE': 'logout_token',
    'LOGOUT_COOKIE_SECURE': True,
    'LOGOUT_COOKIE_HTTP_ONLY': True,
    'LOGOUT_COOKIE_PATH': '/api/logout/',
    'LOGOUT_COOKIE_SAMESITE': env('LOGOUT_COOKIE_SAMESITE'),
    'LOGOUT_COOKIE_TRUSTED_ORIGINS': env('LOGOUT_COOKIE_TRUSTED_ORIGINS').split(','),
}

# csrf cookie settings
CSRF_COOKIE = 'csrftoken'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SAMESITE = env('CSRF_COOKIE_SAMESITE')
CSRF_TRUSTED_ORIGINS = env('CSRF_COOKIE_TRUSTED_ORIGINS').split(',')

# cors policy settings
CORS_ALLOWED_ORIGINS = env('CORS_ALLOWED_ORIGINS').split(',')
CORS_ALLOW_CREDENTIALS = True