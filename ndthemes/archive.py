from datetime import datetime

from django.shortcuts import render
from django.utils import timezone

from cms.models import Page

from .models import ArchivePageExtension, DateTime, Event, PageTag
from .utils import page_sort_date


def filter_pages(pages, filter_value):
    """Filter a page list down to those matching a ``YYYY`` or ``Month YYYY`` string."""
    page_list = []
    is_year_only = len(filter_value) == 4

    for page in pages:
        if page.template == "news_story.html":
            date = page_sort_date(page)
            if not date:
                continue
            match = date.strftime("%Y") == filter_value if is_year_only else date.strftime("%B %Y") == filter_value
            if match:
                page_list.append(page)
        elif page.template == "event_detail.html":
            event = Event.objects.filter(page=page).first()
            if event:
                reference = event.end or event.start
                if not reference:
                    continue
                match = str(reference.year) == filter_value if is_year_only else reference.strftime("%B %Y") == filter_value
                if match:
                    page_list.append(page)
            else:
                dt = DateTime.objects.filter(placeholder__in=page.get_placeholders("en")).first()
                if dt and dt.start_date:
                    match = (
                        dt.start_date.strftime("%Y") == filter_value
                        if is_year_only
                        else dt.start_date.strftime("%B %Y") == filter_value
                    )
                    if match:
                        page_list.append(page)
    return page_list


def get_archives(category=None, filter_value=None):
    if category and category.lower() == "event":
        events = Event.objects.filter(end__lt=datetime.now()).order_by("-end")
        pages = [event.page for event in events if event.page]
    else:
        pages = list(Page.objects.all())
        pages.sort(key=lambda p: page_sort_date(p) or datetime.min.date())

    if filter_value:
        pages = filter_pages(pages, filter_value)

    categories = []
    if category and category != "all":
        for cat in category.split("+"):
            category_tag = PageTag.objects.filter(tag__iexact=cat).first()
            if category_tag:
                categories.append(category_tag)

    archived = []
    for page in pages:
        if category and category.lower() == "event":
            archived.append(page)
            continue

        include_page = True
        archive = ArchivePageExtension.objects.filter(extended_object=page).first()
        if archive and archive.archive_now:
            if categories and category != "all":
                extension = getattr(page, "pagepreviewextension", None)
                if not extension or not any(tag in extension.tags.all() for tag in categories):
                    include_page = False
            if include_page:
                archived.append(page)

    return archived


def get_categories(pages):
    categories = {}
    for page in pages:
        extension = getattr(page, "pagepreviewextension", None)
        if not extension:
            continue
        for tag in extension.tags.filter(archive_category=True):
            categories[tag.tag] = categories.get(tag.tag, 0) + 1
    return categories


def get_years(pages):
    years = {}
    for page in pages:
        if page.template == "news_story.html":
            date = page_sort_date(page)
            if date:
                year = date.strftime("%Y")
                years[year] = years.get(year, 0) + 1
        elif page.template == "event_detail.html":
            event = Event.objects.filter(page=page).first()
            if event:
                reference = event.end or event.start
                if reference:
                    year = str(reference.year)
                    years[year] = years.get(year, 0) + 1
            else:
                dt = DateTime.objects.filter(placeholder__in=page.get_placeholders("en")).first()
                if dt and dt.start_date:
                    year = str(dt.start_date.year)
                    years[year] = years.get(year, 0) + 1
    return years


def get_months(pages):
    months = {}
    for page in pages:
        if page.template == "news_story.html":
            date = page_sort_date(page)
            if date:
                key = date.strftime("%B %Y")
                months[key] = months.get(key, 0) + 1
        elif page.template == "event_detail.html":
            event = Event.objects.filter(page=page).first()
            if event:
                reference = event.end or event.start
                if reference:
                    key = reference.strftime("%B %Y")
                    months[key] = months.get(key, 0) + 1
            else:
                dt = DateTime.objects.filter(placeholder__in=page.get_placeholders("en")).first()
                if dt and dt.start_date:
                    key = dt.start_date.strftime("%B %Y")
                    months[key] = months.get(key, 0) + 1
    return months


def archive(request):
    archives = get_archives()
    categories = get_categories(archives)
    years = get_years(archives)
    months = get_months(archives)
    return render(
        request,
        "archive/archive.html",
        {"pages": archives, "categories": categories, "years": years, "months": months},
    )


def archive_category(request, category):
    archives = get_archives(category=category)
    years = get_years(archives)
    months = get_months(archives)
    return render(
        request,
        "archive/archive_category.html",
        {
            "pages": archives,
            "category": category,
            "years": years,
            "months": months,
            "title": ", ".join(category.split("+")),
        },
    )


def archive_category_drilldown(request, category, filter_value):
    archives = get_archives(category, filter_value)
    archived_pages = []

    for page in archives:
        page_type = "news"
        location = None
        extension = getattr(page, "pagepreviewextension", None)
        date = page_sort_date(page)
        start_date = date
        end_date = date
        sorting_date = timezone.make_aware(datetime.combine(date, datetime.min.time())) if date else None

        if page.template == "event_detail.html":
            page_type = "event"
            event = Event.objects.filter(page=page).first()
            if event:
                date = event.end or event.start
                sorting_date = event.start
                start_date = event.start
                end_date = event.end
                location = event.location
            else:
                dt = DateTime.objects.filter(placeholder__in=page.get_placeholders("en")).first()
                if dt:
                    start_date = dt.start_date
                    end_date = dt.end_date
                    date = dt.end_date or dt.start_date
                    if dt.start_time:
                        sorting_date = datetime.combine(dt.start_date, dt.start_time)
                    else:
                        sorting_date = datetime.combine(dt.start_date, datetime.min.time())
                    sorting_date = timezone.make_aware(sorting_date)

        archived_pages.append(
            {
                "title": page.get_page_title(),
                "url": page.get_absolute_url(),
                "date": date,
                "start_date": start_date,
                "end_date": end_date,
                "image": extension.image if extension else None,
                "image_alt": extension.image_alt if extension else "",
                "image_caption": extension.image_caption if extension else "",
                "summary_caption": extension.summary_caption if extension else "",
                "page_type": page_type,
                "sorting_date": sorting_date,
                "location": location,
            }
        )

    fallback_date = timezone.make_aware(datetime(1900, 1, 1))
    archived_pages = sorted(archived_pages, key=lambda k: k["sorting_date"] or fallback_date)

    return render(
        request,
        "archive/archive_category_list.html",
        {
            "pages": archived_pages,
            "category": category,
            "title": ", ".join(category.split("+")),
            "filter": filter_value,
        },
    )
