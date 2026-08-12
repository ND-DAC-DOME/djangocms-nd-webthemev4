"""
Small helpers bridging django CMS 5 API differences from the v3 ndthemes app.

django CMS 5 removed the old ``Title`` model, ``publisher_is_draft`` and the
draft/public page duality (there is no versioning package installed here, so
every ``PageContent`` is effectively "live" as soon as it is saved). It also
moved ``Placeholder`` to a generic relation (``Placeholder.source``) instead
of a direct FK to ``Page``. These helpers centralize the small amount of
translation code needed so the rest of the app can stay close to the
original v3 logic.
"""
from cms.models import Page, PageContent


def get_page_from_placeholder(placeholder):
    """Return the ``Page`` that owns a placeholder, or ``None``.

    In CMS 3, ``Placeholder.page`` was a direct FK. In CMS 5, placeholders
    are attached to their owner (usually a ``PageContent``) via a generic
    ``source`` relation.
    """
    if placeholder is None:
        return None
    source = getattr(placeholder, "source", None)
    if source is None:
        return None
    if isinstance(source, PageContent):
        return source.page
    return getattr(source, "page", None)


def page_is_self_or_ancestor(candidate, page):
    """True if ``candidate`` is ``page`` or an ancestor of ``page``."""
    if candidate is None or page is None:
        return False
    current = page
    while current is not None:
        if current.pk == candidate.pk:
            return True
        current = current.parent
    return False


def pages_with_template(template_name, queryset=None):
    """Return a ``Page`` queryset for pages whose (current-language) template matches.

    ``Page.template`` is a property in CMS 5 (delegates to ``PageContent``),
    not a database column, so it can't be used directly in ``.filter()``.
    """
    page_ids = (
        PageContent.admin_manager.filter(template=template_name)
        .values_list("page_id", flat=True)
        .distinct()
    )
    pages = queryset if queryset is not None else Page.objects.all()
    return pages.filter(id__in=list(page_ids))


def page_sort_date(page, language="en"):
    """Best-effort "publish" date for a page, used for News/People/Archive ordering.

    Prefers ``PagePreviewExtension.publish_date`` (editable in the Page Meta
    toolbar) and falls back to the page's creation date, since django CMS 5
    no longer has ``Page.publication_date``.
    """
    extension = getattr(page, "pagepreviewextension", None)
    if extension is not None and extension.publish_date:
        return extension.publish_date
    return page.creation_date.date() if page.creation_date else None
