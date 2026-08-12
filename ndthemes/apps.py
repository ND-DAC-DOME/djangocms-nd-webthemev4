from django.apps import AppConfig


def _patch_cms_delete_confirmation_context():
    """django CMS 5 delete views omit Django 6.1's delete_confirmation_max_display."""
    from cms.admin.placeholderadmin import PlaceholderAdmin
    from django.template.response import TemplateResponse

    def _ensure_delete_context(response):
        if isinstance(response, TemplateResponse) and response.context_data is not None:
            response.context_data.setdefault("delete_confirmation_max_display", None)
        return response

    for method_name in ("delete_plugin", "clear_placeholder"):
        original = getattr(PlaceholderAdmin, method_name)

        def make_wrapper(orig):
            def wrapper(self, request, *args, **kwargs):
                return _ensure_delete_context(orig(self, request, *args, **kwargs))

            wrapper.__name__ = orig.__name__
            wrapper.__doc__ = orig.__doc__
            return wrapper

        setattr(PlaceholderAdmin, method_name, make_wrapper(original))


class NdthemesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ndthemes"
    verbose_name = "ND Themes"

    def ready(self):
        # connect signal receivers (search index, event/page title sync,
        # rich text colour scrubbing)
        from . import signals  # noqa: F401
        from .components import cms_plugins  # noqa: F401
        from .richtext import hide_editor_color_tools

        _patch_cms_delete_confirmation_context()
        hide_editor_color_tools()
