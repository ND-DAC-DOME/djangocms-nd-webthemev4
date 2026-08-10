from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.i18n import JavaScriptCatalog

from ndthemes import archive as ndthemes_archive
from ndthemes import events as ndthemes_events
from ndthemes import views as ndthemes_views

handler404 = "ndthemes.views.handler404"

urlpatterns = [
    path("search/", ndthemes_views.search_results, name="search_results"),
    path("manifest.json", ndthemes_views.manifest, name="manifest"),
    path("archive/", ndthemes_archive.archive, name="archive"),
    path("archive/<str:category>/", ndthemes_archive.archive_category, name="archive_category"),
    path(
        "archive/<str:category>/<str:filter_value>/",
        ndthemes_archive.archive_category_drilldown,
        name="archive_category_drilldown",
    ),
    path("events/series/<slug:slug>/", ndthemes_events.recurring_events, name="recurring_events"),
]

urlpatterns += i18n_patterns(
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("filer/", include("filer.urls")),
)

if settings.OKTA_AUTH:
    urlpatterns += [
        path("oidc/", include("mozilla_django_oidc.urls")),
    ]
else:
    urlpatterns += [
        path("accounts/", include("allauth.urls")),
    ]

urlpatterns += i18n_patterns(
    path("", include("cms.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("400/", default_views.bad_request, kwargs={"exception": Exception("Bad Request!")}),
        path("403/", default_views.permission_denied, kwargs={"exception": Exception("Permission Denied")}),
        path("404/", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")}),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
