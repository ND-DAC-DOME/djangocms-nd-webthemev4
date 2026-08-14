"""
Base settings for djangocms-ndthemev4 (Django 6.1 + django CMS 5.1).
"""
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "samplecms"
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))

# Optional Okta authentication (wired in later milestones)
OKTA_AUTH = env.bool("OKTA_AUTH", default=False)

DEBUG = env.bool("DJANGO_DEBUG", False)
TIME_ZONE = "America/Indiana/Indianapolis"
LANGUAGE_CODE = "en"
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]

LANGUAGES = [
    ("en", _("English")),
]
# When False, the default language (LANGUAGE_CODE) is not prefixed in URLs
# (e.g. "/" instead of "/en/"). Override with DJANGO_PREFIX_DEFAULT_LANGUAGE=True.
PREFIX_DEFAULT_LANGUAGE = env.bool("DJANGO_PREFIX_DEFAULT_LANGUAGE", default=False)

# PostgreSQL via DATABASE_URL (required). Docker Compose entrypoint sets this from POSTGRES_* env vars.
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DJANGO_APPS = [
    "djangocms_simple_admin_style",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_celery_beat",
    "cms",
    "menus",
    "treebeard",
    "sekizai",
    "filer",
    "easy_thumbnails",
    "djangocms_versioning",
    "djangocms_text",
    "djangocms_link",
    "djangocms_alias",
    "djangocms_frontend",
    "djangocms_frontend.contrib.accordion",
    "djangocms_frontend.contrib.alert",
    "djangocms_frontend.contrib.badge",
    "djangocms_frontend.contrib.card",
    "djangocms_frontend.contrib.carousel",
    "djangocms_frontend.contrib.collapse",
    "djangocms_frontend.contrib.content",
    "djangocms_frontend.contrib.grid",
    "djangocms_frontend.contrib.icon",
    "djangocms_frontend.contrib.image",
    "djangocms_frontend.contrib.jumbotron",
    "djangocms_frontend.contrib.link",
    "djangocms_frontend.contrib.listgroup",
    "djangocms_frontend.contrib.media",
    "djangocms_frontend.contrib.navigation",
    "djangocms_frontend.contrib.tabs",
    "djangocms_frontend.contrib.utilities",
]

if OKTA_AUTH:
    THIRD_PARTY_APPS += ["mozilla_django_oidc"]

LOCAL_APPS = [
    "ndthemes",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "account_login"
if OKTA_AUTH:
    # allauth urls are not routed when Okta is enabled, so its backend is dropped too.
    AUTHENTICATION_BACKENDS = [
        "django.contrib.auth.backends.ModelBackend",
        "samplecms.auth.NDOIDCAuthBackend",
    ]
    LOGIN_URL = "/oidc/authenticate/"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
    "cms.middleware.utils.ApphookReloadMiddleware",
]

if OKTA_AUTH:
    MIDDLEWARE += ["mozilla_django_oidc.middleware.SessionRefresh"]

STATIC_ROOT = env("DJANGO_STATIC_ROOT", default="/var/staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_ROOT = str(APPS_DIR / "media")
MEDIA_URL = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
                "samplecms.context_processors.site_defaults",
                "ndthemes.context_processors.general_settings",
                "ndthemes.context_processors.navigation_tree",
                "ndthemes.context_processors.news_stories",
                "ndthemes.context_processors.events",
                "ndthemes.context_processors.page_data",
            ],
        },
    }
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "SAMEORIGIN"

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_TIMEOUT = 5

ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")
ADMINS = [("""ND Theme CMS""", "webhelp@nd.edu")]
MANAGERS = ADMINS

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"

# django CMS
CMS_TEMPLATES = (
    ("home.html", _("Home page")),
    ("home_fade.html", _("Home page (fade)")),
    ("home_inset.html", _("Home page (inset)")),
    ("home_container.html", _("Home page (container)")),
    ("home_fullbleed.html", _("Home page (screen / full-bleed)")),
    ("home_sidenav.html", _("Home page (hero + side-nav)")),
    ("page.html", _("Page")),
    ("page_with_sidenav.html", _("Page with side-nav")),
    ("news_landing.html", _("News Landing Page")),
    ("news_story.html", _("News Story")),
    ("event_listing.html", _("Event Listing Page")),
    ("event_detail.html", _("Event Page")),
    ("event_series.html", _("Event Series Page")),
    ("person_page.html", _("Person Page")),
    ("search.html", _("Search Page")),
    ("archive_results.html", _("Archive Results Page")),
)
CMS_PERMISSION = True
TEXT_INLINE_EDITING = True

THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# Celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {
    "ndthemes-auto-archive-events": {
        "task": "ndthemes.auto_archive_events",
        "schedule": 60 * 60,  # hourly
    },
}

# Okta / OIDC
if OKTA_AUTH:
    # Django runs behind the nginx proxy, which terminates TLS.
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    LOGIN_REDIRECT_URL = env("LOGIN_REDIRECT_URL", default="/")
    LOGOUT_REDIRECT_URL = env("LOGOUT_REDIRECT_URL", default="/")

    _OIDC_BASE_URL = env(
        "OIDC_BASE_URL",
        default="https://okta.nd.edu/oauth2/ausxosq06SDdaFNMB356/v1",
    )
    OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID")
    OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET")

    OIDC_OP_AUTHORIZATION_ENDPOINT = f"{_OIDC_BASE_URL}/authorize"
    OIDC_OP_TOKEN_ENDPOINT = f"{_OIDC_BASE_URL}/token"
    OIDC_OP_USER_ENDPOINT = f"{_OIDC_BASE_URL}/userinfo"
    OIDC_OP_JWKS_ENDPOINT = f"{_OIDC_BASE_URL}/keys"
    OIDC_OP_LOGOUT_ENDPOINT = f"{_OIDC_BASE_URL}/logout"
    OIDC_RP_SIGN_ALGO = "RS256"

    # The library defaults to True; ND accounts must be provisioned first.
    OIDC_CREATE_USER = env.bool("DJANGO_OIDC_CREATE_USER", default=False)

    # How often SessionRefresh re-checks the Okta session.
    OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = env.int(
        "DJANGO_OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS",
        default=900,
    )

    # Provider logout needs the ID token, not the access token.
    OIDC_STORE_ID_TOKEN = True
