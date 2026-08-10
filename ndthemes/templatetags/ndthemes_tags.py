"""
Small template filters used by the NDT4 card/list plugin templates.
"""
from django import template

from ..utils import page_sort_date as _page_sort_date

register = template.Library()


@register.filter
def page_sort_date(page):
    """Best-effort "publish" date for a page, for News/People/Archive card meta."""
    if page is None:
        return None
    return _page_sort_date(page)
