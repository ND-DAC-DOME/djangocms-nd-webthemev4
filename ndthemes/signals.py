"""
Signal receivers replacing v3's ``Title``-based and ``post_publish``/
``post_unpublish`` hooks.

django CMS 5 has no ``Title`` model (use ``PageContent``) and, without the
optional versioning package installed, no draft/public publish step: content
is live as soon as it is saved. Search indexing therefore happens whenever a
plugin with ``search_fields`` is saved, rather than at publish time.
"""
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.html import strip_tags

from cms.models import CMSPlugin, PageContent
from djangocms_text.fields import HTMLField
from djangocms_text.models import Text

from .richtext import scrub_document, scrub_inline_styles
from .utils import get_page_from_placeholder


@receiver(post_save, sender=PageContent)
def pagecontent_saved_receiver(sender, instance, **kwargs):
    """Keep an auto-generated Event/EventSeries page's title in sync with the model name."""
    from .models import Event, EventSeries

    page = instance.page
    event = Event.objects.filter(page=page).first()
    if event and instance.title and instance.title != event.name:
        Event.objects.filter(pk=event.pk).update(name=instance.title)
        return

    series = EventSeries.objects.filter(page=page).first()
    if series and instance.title and instance.title != series.name:
        EventSeries.objects.filter(pk=series.pk).update(name=instance.title)


def _indexable_text(value):
    """Normalize plugin field values into plain text for the search index."""
    if value is None:
        return ""
    text = strip_tags(str(value)).strip()
    return " ".join(text.split())


def reindex_page(page):
    from .models import DEFAULT_LANGUAGE, PageContentIndex

    PageContentIndex.objects.filter(page=page).delete()
    for placeholder in page.get_placeholders(DEFAULT_LANGUAGE):
        for plugin in placeholder.get_plugins():
            instance = plugin.get_plugin_instance()[0]
            if instance is None or not hasattr(instance, "search_fields"):
                continue
            for field in instance.search_fields:
                data = _indexable_text(getattr(instance, field, ""))
                if data:
                    PageContentIndex.objects.create(
                        page=page, plugin_id=instance.pk, content=data
                    )


@receiver(post_save)
def plugin_saved_receiver(sender, instance, **kwargs):
    if not isinstance(instance, CMSPlugin) or not hasattr(instance, "search_fields"):
        return
    page = get_page_from_placeholder(instance.placeholder)
    if page:
        reindex_page(page)


@receiver(post_delete, sender=PageContent)
def pagecontent_deleted_receiver(sender, instance, **kwargs):
    from .models import PageContentIndex

    PageContentIndex.objects.filter(page_id=instance.page_id).delete()


@receiver(pre_save, sender=Text)
def text_plugin_scrubbed_receiver(sender, instance, **kwargs):
    """Drop pasted colours and fonts so Text plugins follow the NDT theme tokens."""
    instance.body = scrub_inline_styles(instance.body)
    if instance.json:
        instance.json = scrub_document(instance.json)


_html_field_names = {}


def get_html_field_names(model):
    """Cached tuple of ``HTMLField`` names declared on ``model``."""
    if model not in _html_field_names:
        _html_field_names[model] = tuple(
            field.name for field in model._meta.concrete_fields if isinstance(field, HTMLField)
        )
    return _html_field_names[model]


@receiver(pre_save)
def html_field_scrubbed_receiver(sender, instance, **kwargs):
    """Apply the same scrubbing to component plugins' ``HTMLField`` content."""
    for name in get_html_field_names(sender):
        value = getattr(instance, name, None)
        if value:
            setattr(instance, name, scrub_inline_styles(value))
