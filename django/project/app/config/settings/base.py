"""
Common settings and globals.

See:
    - https://docs.djangoproject.com/en/dev/topics/settings/
    - https://docs.djangoproject.com/en/dev/ref/settings/
"""

import re

import environ

# -------------------------------------
# GENERAL SETUP
# -------------------------------------

# Paths
# =====================================
# Paths here the `environ.Path` which provides a special api around os paths.
#
# How to use:
#
#   # Get the path as a string
#   PROJECT_PATH()
#
#   # Get a sub-directory or file path as a string
#   # Note: This calls the path directly and not through .path
#   PROJECT_PATH("static")
#   PROJECT_PATH("foo.json")
#
#   # Get a path as an environ Path object
#   PROJECT_PATH.path("static")
#
# Docs:
#   - https://github.com/joke2k/django-environ

WORKING_PATH = environ.Path(__file__) - 1

DJANGO_PATH = WORKING_PATH - 4

PROJECT_PATH = DJANGO_PATH.path("project")

APP_PATH = PROJECT_PATH.path("app")

# Env
# =====================================

env = environ.Env()
environ.Env.read_env(DJANGO_PATH(".env"))

# -------------------------------------
# DJANGO CONFIGURATION
# -------------------------------------

# Django Setup
# =====================================

WSGI_APPLICATION = "app.config.wsgi.application"

ROOT_URLCONF = "app.config.urls"

DEBUG = env.bool("DEBUG", default=False)

SITE_ID = 1

# NOTE: DEFAULT_SITE_ID is part of some custom middleware for DjangoCMS,
#       See: app/cms/middleware.py
DEFAULT_SITE_ID = SITE_ID

ADMINS = ()

MANAGERS = ADMINS

FIXTURE_DIRS = (PROJECT_PATH("fixtures"),)

SECRET_KEY = env("SECRET_KEY")

# NOTE: Expects ALLOWED_HOSTS=host1,host2,host3
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

# NOTE: Expects a domain, like www.foobar.com
ENFORCE_HOST = env("ENFORCE_HOST", default="")


# NOTE: Takes seconds, careful with this if site it not under HTTPS
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)

CRSF_COOKIE_SECURE = env.bool("CRSF_COOKIE_SECURE", default=False)

SECURE_BROWSER_XSS_FILTER = env.bool("SECURE_BROWSER_XSS_FILTER", default=False)

X_FRAME_OPTIONS = env("X_FRAME_OPTIONS", default="SAMEORIGIN")

USE_HTTPS_FOR_ASSETS = env.bool("USE_HTTPS_FOR_ASSETS", False)

# Installed Apps
# =====================================
# Order matters, loosely here; i.e., some apps may need to come after others.
# See:
#   * https://goo.gl/DJMuuG
#   * https://goo.gl/55D52S

INSTALLED_APPS = [
    # NOTE: Order matters here
    "django.contrib.auth",
    # NOTE: End of "Order matters..."
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.redirects",
    "django.contrib.admin",
    "django.contrib.gis",
    "django.contrib.gis.geoip2",
    "django_extensions",
    "storages",
    "rest_framework",
    "rest_framework.authtoken",
    "parler",
    "crispy_forms",
    # "menus",
    # "sekizai",
    # "treebeard",
    "filer",
    "easy_thumbnails",
    "corsheaders",
    "app.devoff",
]

# Expects INSTALLED_APPS=foo,bar,baz
INSTALLED_APPS += env.list("INSTALLED_APPS", default=[])

# Middleware
# =====================================
# Note:
#   * Order matters here.
#
# See:
#   * Django Default Middleware:    https://goo.gl/3McLNt
#   * Django i18n Middleware:       https://goo.gl/TkmjJZ
#   * Django WhiteNoise Middleware: https://goo.gl/b5nztY

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
]

MIDDLEWARE += env.list("MIDDLEWARE", default=[])

if ENFORCE_HOST:
    MIDDLEWARE = ["enforce_host.EnforceHostMiddleware"] + MIDDLEWARE

# Databases
# =====================================
# NOTE: DATABASE_URL format:
#       postgres://USER:PASSWORD@HOST:PORT/NAME
#       See: https://github.com/kennethreitz/dj-database-url

DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://postgres:postgres@postgres/postgres"
    )
}

# NOTE: Setting "ENGINE" separately becuase Heroku defaults to postgres://
#       which sets the backend to django.db.backends.postgresql_psycopg2.
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# Geo Django
# =====================================
# See:
#   * GeoDjango Installation: https://goo.gl/ErkUXv
#   * Geolocation with GeoLite2: https://goo.gl/Pk6BDT
#   * GeoLite Databases: https://goo.gl/aHoCRm

GEOIP_PATH = PROJECT_PATH("geo_data")

# Logging
# =====================================

LOG_LEVEL = env("LOG_LEVEL", default="ERROR")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(name)s:%(lineno)s %(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            )
        },
        "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
    },
    "handlers": {
        "stream": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "": {"handlers": ["stream"], "level": LOG_LEVEL},
        "django.db": {"handlers": ["stream"], "level": LOG_LEVEL},
        "z.pool": {"handlers": ["stream"], "level": LOG_LEVEL},
        "django.server": {"handlers": ["stream"], "level": "WARNING"},
        "django": {"handlers": ["stream"], "level": LOG_LEVEL},
        "app.convergys": {"handlers": ["stream"], "level": "DEBUG", "propagate": False},
    },
}

# Templates
# =====================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (APP_PATH("overrides/templates"), "templates"),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            )
        },
    }
]

# Staticfiles
# =====================================

STATIC_ROOT = PROJECT_PATH("collected-static")

STATIC_URL = "/static/"

# Add project/static to staticfile resolution
# Entries here are eligible for `collectstatic` as well
# See:
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic
STATICFILES_DIRS = (PROJECT_PATH("static"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

SERVE_STATIC = False

MEDIA_ROOT = PROJECT_PATH("media")

MEDIA_URL = "/media/"

STATICFILES_STORAGE = env(
    "STATICFILES_STORAGE",
    default="django.contrib.staticfiles.storage.StaticFilesStorage",
)

WHITENOISE_MAX_AGE = env.int("WHITENOISE_MAX_AGE", default=0)

WHITENOISE_KEEP_ONLY_HASHED_FILES = env.bool(
    "WHITENOISE_KEEP_ONLY_HASHED_FILES", default=False
)

# Locale / I18N & L10N
# =====================================

TIME_ZONE = "America/Los_Angeles"

USE_TZ = True

USE_I18N = True

USE_L10N = True

PREFIX_DEFAULT_LANGUAGE = False

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", "English"),
    # Add additional / change languages here
)

LOCALE_PATHS = (PROJECT_PATH("app/web/locale"),)

# Authentication
# =====================================

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Cache
# =====================================

CACHE_TIMEOUT = env("CACHE_TIMEOUT", default=60 * 60)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": CACHE_TIMEOUT,
    }
}

REDIS_URL = env("REDIS_URL", default="")

if REDIS_URL:
    CACHES["default"]["BACKEND"] = "redis_cache.RedisCache"
    CACHES["default"]["LOCATION"] = REDIS_URL


# Celery
# =====================================

CELERY_BROKER_URL = REDIS_URL

CELERY_RESULT_BACKEND = REDIS_URL

# Parler
# =====================================

PARLER_LANGUAGES = {
    # Fix issue with parler and DjangoCMS
    # See: https://goo.gl/Gs33Lm
    1: ({"code": "en"},),
    "default": {"fallback": "en", "hide_untranslated": False},
}

PARLER_DEFAULT_LANGUAGE_CODE = "en"

# Thumbnails
# =====================================

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "easy_thumbnails.processors.filters",
)

# Crispy Forms
# =====================================

CRISPY_TEMPLATE_PACK = "bootstrap4"

# Rest Framework
# =====================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

# Google
# =====================================

GOOGLE_API_KEY = env("GOOGLE_API_KEY", default="")

GTM_CODE = env("GTM_CODE", default="")

# Favicon
# =====================================

FAVICON = {
    "favicon_version": env("FAVICON_VERSION", default=""),
    "favicon_asset_base_path": "/favicon/",
    "favicon_assets": [
        # TODO: Update (see app/favicon/README.md)
        "favicon.ico"
    ],
}

# Django Debug Toolbar
# =====================================
#  See: https://django-debug-toolbar.readthedocs.io/en/latest/index.html


def show_toolbar(request):
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_COLLAPSED": True,
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    "RENDER_PANELS": False,
    "RESULTS_CACHE_SIZE": 5,
}

# NOTE: More panels are available!
#       See: https://django-debug-toolbar.readthedocs.io/en/latest/panels.html
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
]
