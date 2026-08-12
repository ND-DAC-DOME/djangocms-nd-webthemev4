import datetime as DT

from django.db import models, transaction

from cms.api import add_plugin, create_page
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from cms.models import Page
from cms.models.fields import PageField
from cms.models.pluginmodel import CMSPlugin
from djangocms_text.fields import HTMLField

from .images import resize_image
from .utils import get_page_from_placeholder, page_is_self_or_ancestor, pages_with_template

DEFAULT_LANGUAGE = "en"


class PageTag(models.Model):
    tag = models.CharField(max_length=255, unique=True)
    search_category = models.BooleanField(default=False)
    archive_category = models.BooleanField(default=False)

    def __str__(self):
        return self.tag


class PagePreviewExtension(PageExtension):
    image = models.ImageField(null=True, blank=True)
    image_alt = models.CharField(max_length=255, blank=True, null=True)
    image_caption = models.CharField(max_length=255, blank=True, null=True)
    summary_caption = models.CharField(
        max_length=2048,
        blank=True,
        null=True,
        help_text="Shown as summaries in lists and cards linking to this page.",
    )
    tags = models.ManyToManyField(PageTag, blank=True, related_name="pages")
    publish_date = models.DateField(
        blank=True,
        null=True,
        help_text=(
            "Overrides the page's creation date when sorting News/People "
            "listings and archives. django CMS 5 no longer tracks a "
            "separate page publication date."
        ),
    )

    def __str__(self):
        return self.extended_object.get_page_title()

    def copy_relations(self, oldinstance, language):
        for tag in self.tags.all():
            tag.pages.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.pages.add(self)
            tag.save()

    def save(self, *args, **kwargs):
        if self.image:
            content_file = resize_image(self.image)
            self.image.save(self.image.name, content_file, save=False)
        super().save(*args, **kwargs)

    def get_image(self):
        """Return the preview image for cards/lists linking to this page.

        Simplified from v3: rather than reaching into a specific image
        plugin's placeholder, editors set the preview image directly on
        this extension via the "Page Meta" toolbar item. Card plugins
        (M4/M5) may offer their own richer image sources.
        """
        return self.image


extension_pool.register(PagePreviewExtension)


class ArchiveLink(CMSPlugin):
    text = models.CharField(max_length=255)
    optional_tags = models.ManyToManyField(PageTag, blank=True, related_name="archive_link_filters")

    def __str__(self):
        return f"{self.text}"

    def get_tags(self):
        return "+".join([tag.tag for tag in self.optional_tags.all()])

    def copy_relations(self, oldinstance):
        for tag in self.optional_tags.all():
            tag.archive_link_filters.remove(self)
            tag.save()
        for tag in oldinstance.optional_tags.all():
            tag.archive_link_filters.add(self)
            tag.save()


class ArchivePageExtension(PageExtension):
    archive_now = models.BooleanField(default=False)
    schedule_archive = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.extended_object.get_page_title()


extension_pool.register(ArchivePageExtension)


class PageTagPlugin(CMSPlugin):
    def __str__(self):
        return "Page Tags"


class Setting(models.Model):
    SETTING_TYPES = (
        ("text", "Text"),
        ("boolean", "True/False"),
        ("page", "Page"),
    )

    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True, null=True)
    enabled = models.BooleanField(default=True)
    setting_type = models.CharField(max_length=255, choices=SETTING_TYPES, default="text")
    page = PageField(blank=True, null=True)

    def __str__(self):
        return self.key


class Triptych(CMSPlugin):
    title = models.CharField(max_length=255, blank=True, null=True)

    further_reading_link = PageField(null=True, blank=True)
    further_reading_link_text = models.CharField(max_length=255, blank=True, null=True)

    left_card = PageField(null=True, blank=True, related_name="left_card")
    center_card = PageField(null=True, blank=True, related_name="center_card")
    right_card = PageField(null=True, blank=True, related_name="right_card")

    def __str__(self):
        return f"{self.title}"


class DateTime(CMSPlugin):
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_date}"

    def save(self, *args, **kwargs):
        page = get_page_from_placeholder(self.placeholder)
        event = Event.objects.filter(page=page).first() if page else None
        if event:
            event_changed = False
            if self.start_date:
                new_start = DT.datetime.combine(self.start_date, self.start_time or DT.time.min)
                if new_start != event.start:
                    event.start = new_start
                    event_changed = True

            if self.end_date:
                new_end = DT.datetime.combine(self.end_date, self.end_time or DT.time.min)
                if new_end != event.end:
                    event.end = new_end
                    event_changed = True

            if event_changed and not kwargs.get("from_model", False):
                event.save()

        kwargs.pop("from_model", None)
        super().save(*args, **kwargs)


class Location(CMSPlugin):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    google_maps_link = models.CharField(max_length=4096, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        page = get_page_from_placeholder(self.placeholder)
        event = Event.objects.filter(page=page).first() if page else None
        if event:
            event.location = self.name
            event.map_link = self.google_maps_link
            if not kwargs.get("from_model", False):
                event.save()

        kwargs.pop("from_model", None)
        super().save(*args, **kwargs)


class EventsInsert(CMSPlugin):
    title = models.CharField(max_length=255, blank=True, null=True)

    further_reading_link = PageField(null=True, blank=True)
    further_reading_link_text = models.CharField(max_length=255, blank=True, null=True)

    events_after_date = models.DateField(blank=True, null=True)
    events_before_date = models.DateField(blank=True, null=True)

    limit = models.IntegerField(blank=True, null=True)

    tags = models.ManyToManyField(PageTag, blank=True, related_name="event_filters")

    def copy_relations(self, oldinstance):
        for tag in self.tags.all():
            tag.event_filters.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.event_filters.add(self)
            tag.save()

    def __str__(self):
        return f"{self.title}"

    def get_events(self):
        event_pages = pages_with_template("event_detail.html")
        seen = []
        events = []

        for event in event_pages:
            datetime = DateTime.objects.filter(
                placeholder__in=event.get_placeholders(DEFAULT_LANGUAGE),
                start_date__gte=DT.date.today(),
            ).first()

            location = Location.objects.filter(
                placeholder__in=event.get_placeholders(DEFAULT_LANGUAGE)
            ).first()

            archive = ArchivePageExtension.objects.filter(extended_object=event).first()
            if archive and archive.archive_now:
                continue

            if not datetime:
                continue

            if self.events_after_date and datetime.start_date <= self.events_after_date:
                continue
            if self.events_before_date and datetime.start_date >= self.events_before_date:
                continue

            if self.tags.all():
                page_tags = getattr(event, "pagepreviewextension", None)
                if not page_tags or not any(tag in self.tags.all() for tag in page_tags.tags.all()):
                    continue

            if event.pk not in seen:
                events.append(
                    {
                        "title": event.get_page_title(),
                        "date": datetime.start_date,
                        "end_date": datetime.end_date,
                        "start_time": datetime.start_time,
                        "end_time": datetime.end_time,
                        "location": location,
                        "url": event.get_absolute_url(),
                    }
                )
                seen.append(event.pk)

        events.sort(key=lambda x: x["date"])

        if self.limit and len(events) >= self.limit:
            events = events[: self.limit]
        return events


class EventList(CMSPlugin):
    title = models.CharField(max_length=255, blank=True, null=True)
    events_after_date = models.DateField(blank=True, null=True)
    events_before_date = models.DateField(blank=True, null=True)

    child_events_only = models.BooleanField(default=False)

    limit = models.IntegerField(blank=True, null=True)

    tags = models.ManyToManyField(PageTag, blank=True, related_name="event_list_filters")

    view_more_link = PageField(blank=True, null=True, related_name="event_list_view_more_link")
    view_more_link_text = models.CharField(max_length=255, blank=True, null=True)

    def copy_relations(self, oldinstance):
        for tag in self.tags.all():
            tag.event_filters.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.event_filters.add(self)
            tag.save()

    def __str__(self):
        return "Event List"

    def get_events(self):
        current_page = get_page_from_placeholder(self.placeholder)
        event_pages = pages_with_template("event_detail.html")

        if self.child_events_only and current_page:
            event_pages = event_pages.filter(parent=current_page)

        seen = []
        events = []

        for event in event_pages:
            datetime = DateTime.objects.filter(
                placeholder__in=event.get_placeholders(DEFAULT_LANGUAGE),
                end_date__gte=DT.date.today(),
            ).first()

            location = Location.objects.filter(
                placeholder__in=event.get_placeholders(DEFAULT_LANGUAGE)
            ).first()

            archive = ArchivePageExtension.objects.filter(extended_object=event).first()
            if archive and archive.archive_now:
                continue

            if datetime and self.events_after_date and datetime.start_date <= self.events_after_date:
                continue
            if datetime and self.events_before_date and datetime.start_date >= self.events_before_date:
                continue

            if self.tags.all():
                page_tags = getattr(event, "pagepreviewextension", None)
                if not page_tags or not any(tag in self.tags.all() for tag in page_tags.tags.all()):
                    continue

            event_record = Event.objects.filter(page=event).first()

            recurring = False
            if event_record and event_record.recurring_event:
                recurring = event_record.recurring_event.events.count() > 1

            if datetime and event.pk not in seen:
                events.append(
                    {
                        "title": event.get_page_title(),
                        "date": datetime.start_date,
                        "end_date": datetime.end_date,
                        "start_time": datetime.start_time,
                        "end_time": datetime.end_time,
                        "location": location,
                        "url": event.get_absolute_url(),
                        "recurring": recurring,
                        "series": bool(event_record and event_record.series),
                    }
                )
                seen.append(event.pk)

        events.sort(key=lambda x: x["date"])

        if self.limit and len(events) >= self.limit:
            events = events[: self.limit]
        return events


class ChildPageList(CMSPlugin):
    order_choices = (
        ("name-asc", "Title (A → Z)"),
        ("name-desc", "Title (Z → A)"),
        ("date-asc", "Publication Date (Newest → Oldest)"),
        ("date-desc", "Publication Date (Oldest → Newest)"),
    )
    title = models.CharField(max_length=2048, blank=True, null=True)
    tags = models.ManyToManyField(PageTag, blank=True, related_name="child_page_list_filters")

    order = models.CharField(max_length=255, blank=True, null=True, choices=order_choices)
    parent_page = PageField(blank=True, null=True, related_name="child_page_list_parent_page")
    show_publication_date = models.BooleanField(default=False)
    limit = models.IntegerField(blank=True, null=True)
    view_more_link = PageField(blank=True, null=True, related_name="child_page_list_view_more_link")
    view_more_link_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title or "Child Page List"

    def get_children(self):
        parent = self.parent_page or get_page_from_placeholder(self.placeholder)
        if not parent:
            return []
        pages = parent.get_child_pages()

        if self.tags.all():
            pages = pages.filter(pagepreviewextension__tags__in=self.tags.all()).distinct()

        from .utils import page_sort_date

        pages = list(pages)
        if self.order == "name-desc":
            pages.sort(key=lambda p: p.get_page_title(), reverse=True)
        elif self.order == "name-asc":
            pages.sort(key=lambda p: p.get_page_title())
        elif self.order == "date-desc":
            pages.sort(key=lambda p: page_sort_date(p) or DT.date.min, reverse=True)
        else:
            pages.sort(key=lambda p: page_sort_date(p) or DT.date.min)

        if self.limit:
            pages = pages[: self.limit]
        return pages

    def copy_relations(self, oldinstance):
        for tag in self.tags.all():
            tag.child_page_list_filters.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.child_page_list_filters.add(self)
            tag.save()


class ButtonLink(CMSPlugin):
    text = models.CharField(max_length=255)
    link = PageField(blank=True, null=True)
    external_link = models.CharField(max_length=4096, blank=True, null=True)

    def __str__(self):
        return f"{self.text}"


class EmailLink(CMSPlugin):
    text = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.text}"

    @property
    def search_fields(self):
        return ("text", "email")


class SimpleText(CMSPlugin):
    text = models.CharField(max_length=2048)

    def __str__(self):
        return f"{self.text}"

    @property
    def search_fields(self):
        return ("text",)


def _person_pages(placeholder, tags):
    current_page = get_page_from_placeholder(placeholder)
    if not current_page:
        return []
    pages = pages_with_template("person_page.html", queryset=current_page.get_child_pages())

    if tags.all():
        pages = pages.filter(pagepreviewextension__tags__in=tags.all()).distinct()

    people = []
    for page in pages:
        archive = ArchivePageExtension.objects.filter(extended_object=page).first()
        if archive and archive.archive_now:
            continue

        extension = getattr(page, "pagepreviewextension", None)
        position_obj = SimpleText.objects.filter(
            placeholder__in=page.get_placeholders(DEFAULT_LANGUAGE)
        ).first()

        people.append(
            {
                "name": page.get_page_title(),
                "image": extension.image if extension else None,
                "caption": extension.image_caption if extension else "",
                "url": page.get_absolute_url(),
                "position": position_obj.text if position_obj else None,
            }
        )
    return people


def _sort_people(people, order):
    if order == "name-desc":
        people.sort(key=lambda x: x["name"], reverse=True)
    elif order == "position-desc":
        people.sort(key=lambda x: x["position"] or "", reverse=True)
    elif order == "position-asc":
        people.sort(key=lambda x: x["position"] or "")
    else:
        people.sort(key=lambda x: x["name"])
    return people


class PersonListGrid(CMSPlugin):
    order_choices = (
        ("name-asc", "Name (A → Z)"),
        ("name-desc", "Name (Z → A)"),
        ("position-asc", "Position (A → Z)"),
        ("position-desc", "Position (Z → A)"),
    )
    title = models.CharField(max_length=1024, blank=True, null=True)
    tags = models.ManyToManyField(PageTag, blank=True, related_name="person_grid_list_filters")
    order = models.CharField(max_length=255, choices=order_choices, default="name-asc")

    def people(self):
        return _sort_people(_person_pages(self.placeholder, self.tags), self.order)

    def copy_relations(self, oldinstance):
        for tag in self.tags.all():
            tag.person_grid_list_filters.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.person_grid_list_filters.add(self)
            tag.save()

    def __str__(self):
        return "Person List Grid"


class PersonListStacked(CMSPlugin):
    order_choices = PersonListGrid.order_choices
    title = models.CharField(max_length=1024, blank=True, null=True)
    tags = models.ManyToManyField(PageTag, blank=True, related_name="person_list_stacked_filters")
    order = models.CharField(max_length=255, choices=order_choices, default="name-asc")

    def people(self):
        return _sort_people(_person_pages(self.placeholder, self.tags), self.order)

    def copy_relations(self, oldinstance):
        for tag in self.tags.all():
            tag.person_list_stacked_filters.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.person_list_stacked_filters.add(self)
            tag.save()

    def __str__(self):
        return "Person List Stacked"


class PersonListItem(CMSPlugin):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    title = models.CharField(max_length=255)
    summary = models.TextField()

    def __str__(self):
        return f"{self.name}"


class SideNavigationChildList(CMSPlugin):
    order_choices = (
        ("page-tree", "Page Order"),
        ("name-asc", "Title (A → Z)"),
        ("name-desc", "Title (Z → A)"),
        ("date-asc", "Publication Date (Newest → Oldest)"),
        ("date-desc", "Publication Date (Oldest → Newest)"),
    )
    tags = models.ManyToManyField(PageTag, blank=True, related_name="side_navigation_child_list_filters")
    link_order = models.CharField(max_length=255, blank=True, null=True, choices=order_choices, default="page-tree")
    show_second_level_children = models.BooleanField(
        default=False,
        help_text="When enabled, nested links appear only under the current section branch.",
    )
    child_link_order = models.CharField(max_length=255, blank=True, null=True, choices=order_choices, default="page-tree")

    def _ordered(self, pages, order):
        from .utils import page_sort_date

        pages = list(pages)
        if order == "name-desc":
            pages.sort(key=lambda x: x.get_page_title(), reverse=True)
        elif order == "name-asc":
            pages.sort(key=lambda x: x.get_page_title())
        elif order == "date-desc":
            pages.sort(key=lambda x: page_sort_date(x) or DT.date.min, reverse=True)
        elif order == "date-asc":
            pages.sort(key=lambda x: page_sort_date(x) or DT.date.min)
        else:
            pages.sort(key=lambda x: x.path)
        return pages

    def get_siblings(self):
        current_page = get_page_from_placeholder(self.placeholder)
        if not current_page:
            return []

        if current_page.parent is None:
            pages = current_page.get_child_pages()
        elif current_page.parent.parent is not None:
            pages = current_page.parent.parent.get_child_pages()
        else:
            pages = current_page.parent.get_child_pages()

        if self.tags.all():
            pages = pages.filter(pagepreviewextension__tags__in=self.tags.all()).distinct()

        pages = self._ordered(pages, self.link_order)

        language = current_page.get_content_obj().language
        pages = [
            page
            for page in pages
            if page.get_content_obj(language).in_navigation
        ]

        page_list = []
        for page in pages:
            branch_active = page_is_self_or_ancestor(page, current_page)
            page_list.append(
                {
                    "page": page,
                    "active": branch_active,
                    "current": page == current_page,
                    "children": [],
                }
            )
            if self.show_second_level_children and branch_active:
                children = self._ordered(page.get_child_pages(), self.child_link_order)
                for child in children:
                    if not child.get_content_obj(language).in_navigation:
                        continue
                    page_list[-1]["children"].append(
                        {
                            "page": child,
                            "active": page_is_self_or_ancestor(child, current_page),
                            "current": child == current_page,
                        }
                    )
        return page_list

    def copy_relations(self, oldinstance):
        for tag in self.tags.all():
            tag.side_navigation_child_list_filters.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.side_navigation_child_list_filters.add(self)
            tag.save()

    def __str__(self):
        return "Side Navigation Child List"


class SideNavigationRootList(CMSPlugin):
    """Side-nav links from children of the site root (top-level navigation)."""

    order_choices = (
        ("page-tree", "Page Order"),
        ("name-asc", "Title (A → Z)"),
        ("name-desc", "Title (Z → A)"),
        ("date-asc", "Publication Date (Newest → Oldest)"),
        ("date-desc", "Publication Date (Oldest → Newest)"),
    )
    tags = models.ManyToManyField(PageTag, blank=True, related_name="side_navigation_root_list_filters")
    link_order = models.CharField(max_length=255, blank=True, null=True, choices=order_choices, default="page-tree")
    show_second_level_children = models.BooleanField(
        default=False,
        help_text="When enabled, nested links appear only under the current section branch.",
    )
    child_link_order = models.CharField(max_length=255, blank=True, null=True, choices=order_choices, default="page-tree")

    def _ordered(self, pages, order):
        from .utils import page_sort_date

        pages = list(pages)
        if order == "name-desc":
            pages.sort(key=lambda x: x.get_page_title(), reverse=True)
        elif order == "name-asc":
            pages.sort(key=lambda x: x.get_page_title())
        elif order == "date-desc":
            pages.sort(key=lambda x: page_sort_date(x) or DT.date.min, reverse=True)
        elif order == "date-asc":
            pages.sort(key=lambda x: page_sort_date(x) or DT.date.min)
        else:
            pages.sort(key=lambda x: x.path)
        return pages

    def get_root_items(self):
        current_page = get_page_from_placeholder(self.placeholder)
        if not current_page:
            return []

        root_page = current_page
        while root_page.parent is not None:
            root_page = root_page.parent

        pages = root_page.get_child_pages()

        if self.tags.all():
            pages = pages.filter(pagepreviewextension__tags__in=self.tags.all()).distinct()

        pages = self._ordered(pages, self.link_order)

        language = current_page.get_content_obj().language
        pages = [
            page
            for page in pages
            if page.get_content_obj(language).in_navigation
        ]

        page_list = []
        for page in pages:
            branch_active = page_is_self_or_ancestor(page, current_page)
            page_list.append(
                {
                    "page": page,
                    "active": branch_active,
                    "current": page == current_page,
                    "children": [],
                }
            )
            if self.show_second_level_children and branch_active:
                children = self._ordered(page.get_child_pages(), self.child_link_order)
                for child in children:
                    if not child.get_content_obj(language).in_navigation:
                        continue
                    page_list[-1]["children"].append(
                        {
                            "page": child,
                            "active": page_is_self_or_ancestor(child, current_page),
                            "current": child == current_page,
                        }
                    )
        return page_list

    def copy_relations(self, oldinstance):
        for tag in self.tags.all():
            tag.side_navigation_root_list_filters.remove(self)
            tag.save()
        for tag in oldinstance.tags.all():
            tag.side_navigation_root_list_filters.add(self)
            tag.save()

    def __str__(self):
        return "Side Navigation Root List"


class SideNavigationPageLink(CMSPlugin):
    page = PageField(blank=True, null=True, related_name="side_navigation_page_link", on_delete=models.SET_NULL)
    text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.text:
            return f"{self.text}"
        return self.page.get_page_title() if self.page else "Side Navigation Page Link"


class SideNavigationDynamicFilter(CMSPlugin):
    def __str__(self):
        return "Side Navigation Dynamic Filter"


class Ribbon(CMSPlugin):
    internal_link = PageField(blank=True, null=True)
    external_link = models.CharField(max_length=4096, blank=True, null=True)
    link_text = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=4096, blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled Ribbon"


class RibbonImage(CMSPlugin):
    image = models.ImageField(blank=True, null=True)
    internal_link = PageField(blank=True, null=True)
    external_link = models.CharField(max_length=4096, blank=True, null=True)
    link_text = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=4096, blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled Ribbon with Image"


class RibbonImageAlt(CMSPlugin):
    image = models.ImageField(blank=True, null=True)
    internal_link = PageField(blank=True, null=True)
    external_link = models.CharField(max_length=4096, blank=True, null=True)
    link_text = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=4096, blank=True, null=True)

    def __str__(self):
        return self.title or "Untitled Alt Ribbon with Image"


class PageContentIndex(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    plugin_id = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.page.get_page_title()}"


class PhoneNumber(CMSPlugin):
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.phone_number}"


class ExternalLink(CMSPlugin):
    title = models.CharField(max_length=4096)
    link = models.CharField(max_length=4096)
    description = HTMLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class FullWidthImage(CMSPlugin):
    image = models.ImageField()
    caption = models.CharField(max_length=4096, blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.caption}"


class EventSeries(models.Model):
    name = models.CharField(max_length=1024)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name="event_series_record")

    class Meta:
        verbose_name_plural = "Event Series"

    def __str__(self):
        return f"{self.name}"

    def delete(self, *args, **kwargs):
        if self.page:
            self.page.delete()
        for event in self.events.all():
            event.delete()
        super().delete(*args, **kwargs)

    def _slug(self):
        event_count = EventSeries.objects.filter(name=self.name).exclude(pk=self.pk).count()
        slug = self.name.lower().replace(" ", "-").replace(":", "-").replace("!", "")
        if event_count > 0:
            slug = f"{slug}-{event_count}"
        return slug

    def save(self, *args, **kwargs):
        kwargs.pop("new_start", None)
        kwargs.pop("new_end", None)
        kwargs.pop("from_event", None)

        if not self.page:
            self.page = create_page(
                title=self.name,
                template="event_series.html",
                slug=self._slug(),
                language=DEFAULT_LANGUAGE,
                in_navigation=False,
            )

            extension = PagePreviewExtension()
            extension.extended_object = self.page
            extension.save()

            tag = PageTag.objects.filter(tag="Event").first()
            if tag:
                extension.tags.add(tag)
                extension.save()

        placeholder = self.page.get_placeholders(DEFAULT_LANGUAGE).filter(slot="Series Events").first()
        if placeholder and placeholder.get_plugins().count() == 0:
            add_plugin(placeholder, "EventListPlugin", DEFAULT_LANGUAGE, position="last-child", child_events_only=True)

        content = self.page.pagecontent_set(manager="admin_manager").filter(language=DEFAULT_LANGUAGE).first()
        if content and content.page_title != self.name:
            content.page_title = self.name
            content.menu_title = self.name
            content.title = self.name
            content.save()

        if not self.page.parent:
            event_page = Setting.objects.filter(key="Event Page").first()
            if event_page and event_page.page:
                with transaction.atomic():
                    self.page.move_page(event_page.page)

        super().save(*args, **kwargs)


class RecurringEvent(models.Model):
    pass


class Event(models.Model):
    name = models.CharField(max_length=1024)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=1024, blank=True, null=True)
    map_link = models.CharField(max_length=4096, blank=True, null=True)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name="event_record")
    recurring_event = models.ForeignKey(RecurringEvent, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")
    series = models.ForeignKey(EventSeries, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")

    def __str__(self):
        return f"{self.name}: {self.start}"

    def delete(self, *args, **kwargs):
        if self.page:
            self.page.delete()
        super().delete(*args, **kwargs)

    def _slug(self):
        event_count = Event.objects.filter(name=self.name).exclude(pk=self.pk).count()
        slug = self.name.lower().replace(" ", "-").replace(":", "-").replace("!", "")
        if event_count > 0:
            slug = f"{slug}-{event_count}"
        return slug

    def save(self, *args, **kwargs):
        previous_series = None
        if self.pk:
            previous_series = Event.objects.filter(pk=self.pk).values_list("series_id", flat=True).first()

        if not self.page:
            self.page = create_page(
                title=self.name,
                template="event_detail.html",
                slug=self._slug(),
                language=DEFAULT_LANGUAGE,
                in_navigation=False,
            )

            extension = PagePreviewExtension()
            extension.extended_object = self.page
            extension.save()

            tag = PageTag.objects.filter(tag="Event").first()
            if tag:
                extension.tags.add(tag)
                extension.save()

        placeholders = {
            placeholder.slot: placeholder
            for placeholder in self.page.get_placeholders(DEFAULT_LANGUAGE)
        }

        datetime_placeholder = placeholders.get("date_time")
        if datetime_placeholder:
            existing = datetime_placeholder.get_plugins().first()
            if existing:
                datetime_plugin = DateTime.objects.get(id=existing.id)
                if self.start:
                    datetime_plugin.start_date = self.start.date()
                    datetime_plugin.start_time = self.start.time()
                if self.end:
                    datetime_plugin.end_date = self.end.date()
                    datetime_plugin.end_time = self.end.time()
                datetime_plugin.save(from_model=True)
            elif self.start:
                kwargs_dt = {"start_date": self.start.date(), "start_time": self.start.time()}
                if self.end:
                    kwargs_dt.update({"end_date": self.end.date(), "end_time": self.end.time()})
                add_plugin(datetime_placeholder, "DateTimePlugin", DEFAULT_LANGUAGE, position="last-child", **kwargs_dt)
            else:
                add_plugin(datetime_placeholder, "DateTimePlugin", DEFAULT_LANGUAGE, position="last-child")

        location_placeholder = placeholders.get("location")
        if location_placeholder:
            existing = location_placeholder.get_plugins().first()
            if existing:
                location_plugin = Location.objects.get(id=existing.id)
                location_plugin.name = self.location
                location_plugin.address = self.location
                location_plugin.google_maps_link = self.map_link
                location_plugin.save(from_model=True)
            else:
                add_plugin(
                    location_placeholder,
                    "LocationPlugin",
                    DEFAULT_LANGUAGE,
                    position="last-child",
                    name=self.location,
                    address=self.location,
                    google_maps_link=self.map_link,
                )

        content_placeholder = placeholders.get("content")
        if content_placeholder and content_placeholder.get_plugins().count() == 0:
            add_plugin(content_placeholder, "TextPlugin", DEFAULT_LANGUAGE, position="last-child", body="This is a description of the event.")

        content = self.page.pagecontent_set(manager="admin_manager").filter(language=DEFAULT_LANGUAGE).first()
        if content and content.page_title != self.name:
            content.page_title = self.name
            content.menu_title = self.name
            content.title = self.name
            content.save()

        if not self.page.parent:
            with transaction.atomic():
                if self.series:
                    self.page.move_page(self.series.page)
                else:
                    event_page = Setting.objects.filter(key="Event Page").first()
                    if event_page and event_page.page:
                        self.page.move_page(event_page.page)

        if previous_series is not None and previous_series != self.series_id:
            with transaction.atomic():
                if self.series:
                    self.page.move_page(self.series.page)
                else:
                    event_page = Setting.objects.filter(key="Event Page").first()
                    if event_page and event_page.page:
                        self.page.move_page(event_page.page)

        if self.series:
            self.series.save(new_start=self.start, new_end=self.end, from_event=self)

        super().save(*args, **kwargs)


# M5 NDT component plugin models (discovered by migrations)
from .components.models import (  # noqa: E402,F401
    Accordion,
    AccordionItem,
    Heading,
    List,
    ListItem,
    Notice,
    Quote,
    Stat,
    StatList,
    TabPanel,
    Table,
    Tabs,
    Timeline,
    TimelineItem,
    Avatar,
    Banner,
    BannerAccordionItem,
    BannerImageItem,
    Button,
    ButtonGroup,
    ButtonItem,
    ButtonList,
    Byline,
    CardBylineItem,
    CardDefault,
    CardEvent,
    CardFeatured,
    CardGrid,
    CardList,
    CardMediaMention,
    CardMediaMentionQuoted,
    CardNews,
    CardPerson,
    Dialog,
    FAQ,
    FAQItem,
    FootnoteItem,
    FootnoteList,
    Form,
    FormField,
    Gallery,
    GalleryItem,
    Icon,
    ImageMultiple,
    ImageMultipleItem,
    ImageSingle,
    IconButton,
    LedeButton,
    NavAnchor,
    NavAnchorItem,
    PageHeader,
    Pagination,
    PaginationItem,
    SearchForm,
    SocialShare,
    Sticker,
    Video,
    VideoButton,
)
