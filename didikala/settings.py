from django.utils.translation import gettext_lazy as _
from pathlib import Path
import gettext
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ct@f(94xoj=hqs1$8l&$#*uu_y1_hu&hn*#c$r-yxd(_n3pg=&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # Created apps
    'apps.main.apps.MainConfig',
    'apps.account.apps.AccountConfig',
    'apps.address.apps.AddressConfig',
    'apps.product.apps.ProductConfig',
    'apps.cart.apps.CartConfig',
    'apps.order.apps.OrderConfig',

    # Django modules
    'django_cleanup.apps.CleanupConfig',
    'azbankgateways',
    'django_jalali',
    'widget_tweaks',
    'ckeditor',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "didikala.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "contexts.context_processors.header_cart",
            ],
        },
    },
]

WSGI_APPLICATION = "didikala.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Login settings
LOGIN_URL = "/account/login"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "fa-ir"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "assets")]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = 'account.User'

# Django auth backends
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'apps.account.auth.EmailAuthenticationBackend', ]

# Add farsi language for Internationalization
LANGUAGES = (
    ('fa', _('Persian')),
)

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# BankGateways settings
AZ_IRANIAN_BANK_GATEWAYS = {
   'GATEWAYS': {
       'IDPAY': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'METHOD': 'POST',  # GET or POST
           'SANDBOX': 1,  # 0 disable, 1 active
       },
       'ZARINPAL': {
           'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
           'SANDBOX': 1,  # 0 disable, 1 active
       },
   },
   'IS_SAMPLE_FORM_ENABLE': True,  # Optional(default is False)
   'DEFAULT': 'ZARINPAL',  # Required
   'CURRENCY': 'IRR',  # Optional
   'TRACKING_CODE_QUERY_PARAM': 'tc',  # Optional
   'TRACKING_CODE_LENGTH': 16,  # Optional
   'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',  # Optional
   'BANK_PRIORITIES': ['ZARINPAL', 'IDPAY']
}
