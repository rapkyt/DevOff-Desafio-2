import logging

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve

log = logging.getLogger(__name__)


admin.autodiscover()

# -------------------------------------
# URLS CONFIG
# -------------------------------------
# See: https://docs.djangoproject.com/en/dev/topics/http/urls/#example

js_catalog_pkgs = ()

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "jsi18n/",
        JavaScriptCatalog.as_view(packages=js_catalog_pkgs),
        name="javascript-catalog",
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("app.devoff.urls", namespace="devoff"))
]

# Localized URLs
# =====================================

urlpatterns = i18n_patterns(
    *urlpatterns, prefix_default_language=settings.PREFIX_DEFAULT_LANGUAGE
)


# Non-Localized URLs
# =====================================


# -------------------------------------
# Debug URLs
# -------------------------------------

if settings.DEBUG:
    # Per latest django debug toolbar
    # See:
    # http://django-debug-toolbar.readthedocs.io/en/stable/installation.html
    try:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

        # Serve media files when DEBUG=True
        urlpatterns = (
            [
                re_path(
                    "media/(?P<path>.*)$",
                    serve,
                    {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
                )
            ]
            + staticfiles_urlpatterns()
            + urlpatterns
        )
    except ImportError:
        log.debug("Could not activate debug toolbar.")
