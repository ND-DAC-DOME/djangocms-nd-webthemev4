import datetime

from .models import ArchivePageExtension, DateTime, Location, Setting
from .utils import page_is_self_or_ancestor, pages_with_template
from cms.models.contentmodels import PageContent


def navigation_tree(request):
    """Sidebar navigation tree rooted at the top-most ancestor of the current page."""
    root_page = getattr(request, "current_page", None)
    if not root_page:
        return {}

    while root_page.parent is not None:
        root_page = root_page.parent

    nav_tree = []
    for child in root_page.get_child_pages():
        content = child.get_content_obj(request.LANGUAGE_CODE, fallback=False)
        if not content or not content.in_navigation:
            continue

        branch_active = page_is_self_or_ancestor(child, request.current_page)
        child_obj = {
            "title": child.get_page_title(),
            "url": child.get_absolute_url(),
            "children": [],
            "active": branch_active,
        }

        if branch_active:
            for grandchild in child.get_child_pages():
                grandchild_content = grandchild.get_content_obj(request.LANGUAGE_CODE, fallback=False)
                if not grandchild_content or not grandchild_content.in_navigation:
                    continue
                child_obj["children"].append(
                    {
                        "title": grandchild.get_page_title(),
                        "url": grandchild.get_absolute_url(),
                        "active": page_is_self_or_ancestor(grandchild, request.current_page),
                    }
                )
        nav_tree.append(child_obj)

    return {"sidebar_navigation": nav_tree}


def news_stories(request):
    current_page = getattr(request, "current_page", None)
    if not current_page:
        return {}

    stories = []
    for child in current_page.get_child_pages():
        if not child.get_content_obj(request.LANGUAGE_CODE):
            continue
        archive = ArchivePageExtension.objects.filter(extended_object=child).first()
        if archive and archive.archive_now:
            continue
        if child.template != "news_story.html":
            continue

        extension = getattr(child, "pagepreviewextension", None)
        stories.append(
            {
                "title": child.get_page_title(),
                "url": child.get_absolute_url(),
                "date": extension.publish_date if extension else None,
                "image": extension.image if extension else None,
                "image_alt": extension.image_alt if extension else "",
                "image_caption": extension.image_caption if extension else "",
                "summary_caption": extension.summary_caption if extension else "",
            }
        )

    return {"news_stories": stories}


def general_settings(request):
    context = {}

    if not Setting.objects.filter(key="Site Description").exists():
        Setting.objects.create(key="Site Description", value="An awesome Content Management System for Research.")

    for setting in Setting.objects.filter(enabled=True):
        context[setting.key.lower().replace(" ", "_")] = setting.value

    context["current_year"] = datetime.datetime.now().year
    return context


def events(request):
    if not getattr(request, "current_page", None):
        return {}

    event_list = []
    seen = []
    for event_page in pages_with_template("event_detail.html"):
        if not event_page.get_content_obj(request.LANGUAGE_CODE):
            continue

        placeholders = event_page.get_placeholders(request.LANGUAGE_CODE)
        datetime_obj = DateTime.objects.filter(placeholder__in=placeholders).first()
        location = Location.objects.filter(placeholder__in=placeholders).first()

        if datetime_obj and event_page.pk not in seen:
            event_list.append(
                {
                    "title": event_page.get_page_title(),
                    "date": datetime_obj.start_date,
                    "end_date": datetime_obj.end_date,
                    "start_time": datetime_obj.start_time,
                    "end_time": datetime_obj.end_time,
                    "location": location,
                    "url": event_page.get_absolute_url(),
                }
            )
            seen.append(event_page.pk)

    return {"events": event_list}


def page_data(request):
    current_page = getattr(request, "current_page", None)
    if not current_page:
        return {}

    context = {}
    try:
        placeholders = current_page.get_placeholders(request.LANGUAGE_CODE)
    except PageContent.DoesNotExist:
        # If there is no versioned content for the current language, default to an empty list
        # or attempt to get fallbacks if your logic requires it.
        placeholders = []

    datetime_obj = DateTime.objects.filter(placeholder__in=placeholders).first()
    if datetime_obj:
        context["datetime"] = datetime_obj

    location = Location.objects.filter(placeholder__in=placeholders).first()
    if location:
        context["location"] = location

    root_page = current_page
    while root_page.parent is not None:
        root_page = root_page.parent

    return {"page_data": context, "root_page": root_page}
