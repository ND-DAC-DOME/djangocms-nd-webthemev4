"""
Seed M4 plugin showcase pages and supporting demo content.

Builds two review pages exercising all 23 ndthemes plugins with NDT4 markup,
plus optional person-page children for the Person List plugins. Safe to re-run:
showcase placeholders are cleared and rebuilt each time.

Usage:
    python manage.py seed_plugin_showcase
    python manage.py seed_plugin_showcase --no-people
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cms.api import add_plugin, create_page
from cms.models import Page

from ndthemes.models import DateTime, PagePreviewExtension, PageTag
from ndthemes.seed.helpers import (
    clear_placeholder,
    fixture_path,
    move_under_parent,
    page_by_title,
    save_plugin_image,
    set_preview_image,
)

FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "m4_demo" / "images"


def get_or_create_page(title, template, parent=None, in_navigation=False):
    page = page_by_title(title)
    if page:
        return page
    kwargs = {"title": title, "template": template, "language": "en", "in_navigation": in_navigation}
    if parent:
        kwargs["parent"] = parent
    return create_page(**kwargs)


class Command(BaseCommand):
    help = "Seed Plugin Showcase pages and demo content for M4 plugin QA."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-people",
            action="store_true",
            help="Skip creating person-page children under the showcase.",
        )

    def handle(self, *args, **options):
        home = Page.objects.filter(is_home=True).first()
        if not home:
            raise CommandError("No home page found. Run `python manage.py goirish` first.")

        self.stdout.write("Ensuring sample pages for card/triptych demos...")
        sample_page = get_or_create_page("Sample Page", "page.html", parent=home)
        sample_news = get_or_create_page("Sample News Story", "news_story.html", parent=home)
        news_breakthrough = get_or_create_page(
            "Notre Dame Researchers Announce Breakthrough",
            "news_story.html",
            parent=home,
        )
        sample_event = get_or_create_page("Sample Event", "event_detail.html", parent=home)
        sample_person = get_or_create_page("Sample Person", "person_page.html", parent=home)
        jane_doe = get_or_create_page("Jane Doe", "person_page.html", parent=home)

        set_preview_image(
            sample_page,
            "campus1.jpg",
            alt="Campus quad",
            summary="A sample interior page used to exercise Triptych and Child Page List cards.",
        )
        set_preview_image(
            sample_news,
            "campus1.jpg",
            alt="Campus quad",
            summary="A short teaser summary shown on News cards and the Triptych/Child Page List plugins.",
        )
        set_preview_image(
            news_breakthrough,
            "campus3.jpg",
            alt="Research lab",
            summary="Notre Dame researchers announce a new breakthrough discovery.",
        )
        set_preview_image(sample_person, "profile1.jpg", alt="Portrait of a Notre Dame faculty member")
        set_preview_image(jane_doe, "profile1.jpg", alt="Portrait of Jane Doe")

        news_tag, _ = PageTag.objects.get_or_create(tag="News")
        for page in (sample_news, news_breakthrough):
            PagePreviewExtension.objects.get(extended_object=page).tags.add(news_tag)

        people_tag, _ = PageTag.objects.get_or_create(tag="People")
        for page in (sample_person, jane_doe):
            PagePreviewExtension.objects.get(extended_object=page).tags.add(people_tag)

        self._fix_demo_event_times()

        self.stdout.write("Building Plugin Showcase page...")
        showcase = page_by_title("Plugin Showcase")
        if not showcase:
            showcase = create_page(
                title="Plugin Showcase",
                template="page.html",
                language="en",
                in_navigation=False,
            )
        move_under_parent(showcase, home)
        self._seed_showcase_content(showcase, home, sample_page, sample_news, news_breakthrough, sample_event)
        self.stdout.write(self.style.SUCCESS(f"  {showcase.get_absolute_url()}"))

        self.stdout.write("Building Plugin Showcase - Side Nav page...")
        showcase_sidenav = page_by_title("Plugin Showcase - Side Nav")
        if not showcase_sidenav:
            showcase_sidenav = create_page(
                title="Plugin Showcase - Side Nav",
                template="page_with_sidenav.html",
                language="en",
                in_navigation=False,
            )
        move_under_parent(showcase_sidenav, home)
        self._seed_showcase_sidenav(showcase_sidenav, sample_event)
        self.stdout.write(self.style.SUCCESS(f"  {showcase_sidenav.get_absolute_url()}"))

        if not options["no_people"]:
            self.stdout.write("Ensuring person-page children for Person List plugins...")
            self._seed_showcase_people(showcase)

        self.stdout.write(self.style.SUCCESS("Plugin showcase seed complete."))

    def _fix_demo_event_times(self):
        """Correct known-bad demo event DateTime data (end before start)."""
        for page_title in ("Test Lecture 2",):
            page = page_by_title(page_title)
            if not page:
                continue
            dt = DateTime.objects.filter(placeholder__in=page.get_placeholders("en")).first()
            if dt and dt.start_time and dt.end_time and dt.end_time <= dt.start_time:
                dt.end_time = dt.end_time.replace(hour=19, minute=30)
                dt.save()

    def _seed_showcase_content(self, showcase, home, sample_page, sample_news, news_breakthrough, sample_event):
        placeholder = clear_placeholder(showcase, "Page Content")

        add_plugin(
            placeholder,
            "TriptychPlugin",
            "en",
            position="last-child",
            title="Triptych (internal pages)",
            left_card=sample_page,
            center_card=sample_news,
            right_card=news_breakthrough,
            further_reading_link=sample_page,
            further_reading_link_text="See all pages",
        )

        add_plugin(
            placeholder,
            "RibbonPlugin",
            "en",
            position="last-child",
            title="Ribbon (text only)",
            caption="A simple text-and-button banner, styled after the NDT4 Banner (Stacked) component.",
            internal_link=sample_page,
            link_text="Learn more",
        )

        add_plugin(placeholder, "RibbonImagePlugin", "en", position="last-child")
        ribbon_image = (
            placeholder.get_plugins().filter(plugin_type="RibbonImagePlugin").first().get_plugin_instance()[0]
        )
        save_plugin_image(ribbon_image, "image", "campus3.jpg")
        ribbon_image.title = "Ribbon with Image (full-bleed)"
        ribbon_image.caption = "Full-bleed dark overlay banner, styled after the NDT4 Banner (Full) component."
        ribbon_image.internal_link = sample_event
        ribbon_image.link_text = "View sample event"
        ribbon_image.save()

        add_plugin(placeholder, "RibbonImageAltPlugin", "en", position="last-child")
        ribbon_alt = (
            placeholder.get_plugins().filter(plugin_type="RibbonImageAltPlugin").first().get_plugin_instance()[0]
        )
        save_plugin_image(ribbon_alt, "image", "campus1.jpg")
        ribbon_alt.title = "Ribbon with Image (alt, side-by-side)"
        ribbon_alt.caption = "Side-by-side light banner, styled after the NDT4 Banner (Default) component."
        ribbon_alt.external_link = "https://nd.edu"
        ribbon_alt.link_text = "Visit nd.edu"
        ribbon_alt.save()

        add_plugin(placeholder, "FullWidthImagePlugin", "en", position="last-child")
        fwi = placeholder.get_plugins().filter(plugin_type="FullWidthImagePlugin").first().get_plugin_instance()[0]
        save_plugin_image(fwi, "image", "campus3.jpg")
        fwi.alt_text = "Full width campus image"
        fwi.caption = "Image (Single) plugin, full width."
        fwi.save()

        add_plugin(placeholder, "EventsPlugin", "en", position="last-child", title="Events Insert")
        add_plugin(placeholder, "EventListPlugin", "en", position="last-child", title="Event List")

        add_plugin(
            placeholder,
            "ChildPageListPlugin",
            "en",
            position="last-child",
            title="Child Page List",
            parent_page=home,
            show_publication_date=True,
            view_more_link=sample_page,
            view_more_link_text="View all pages",
        )

        add_plugin(placeholder, "PersonGridListPlugin", "en", position="last-child", title="Person List (Grid)")
        add_plugin(placeholder, "PersonListStackedPlugin", "en", position="last-child", title="Person List (Stacked)")

        add_plugin(
            placeholder,
            "PersonListItemPlugin",
            "en",
            position="last-child",
            name="Rev. Robert A. Dowd, C.S.C.",
            title="President of the University of Notre Dame",
            summary="Standalone Person List Item plugin, for spotlighting a single person outside the normal person-page listing.",
        )
        person_item = (
            placeholder.get_plugins().filter(plugin_type="PersonListItemPlugin").first().get_plugin_instance()[0]
        )
        save_plugin_image(person_item, "image", "profile1.jpg")
        person_item.save()

        add_plugin(
            placeholder,
            "ExternalLinkPlugin",
            "en",
            position="last-child",
            title="Notre Dame researchers find breakthrough in renewable energy storage",
            link="https://news.nd.edu/",
            description="<p>Researchers at the University of Notre Dame have developed a new method for storing renewable energy.</p>",
        )

        add_plugin(
            placeholder, "ButtonLinkPlugin", "en", position="last-child", text="Button Link (internal)", link=sample_page
        )
        add_plugin(
            placeholder,
            "ButtonLinkPlugin",
            "en",
            position="last-child",
            text="Button Link (external)",
            external_link="https://nd.edu",
        )
        add_plugin(placeholder, "EmailLinkPlugin", "en", position="last-child", text="Email Us", email="webteam@nd.edu")
        add_plugin(placeholder, "PhoneNumberPlugin", "en", position="last-child", phone_number="574-631-5000")
        add_plugin(placeholder, "ArchiveLinkPlugin", "en", position="last-child", text="View the Archive")

        add_plugin(
            placeholder,
            "SimpleTextPlugin",
            "en",
            position="last-child",
            text="This is a Simple Text plugin, used for short inline copy (and for person-page position/title text).",
        )

        add_plugin(placeholder, "PageTagPluginPlugin", "en", position="last-child")

    def _seed_showcase_sidenav(self, showcase_sidenav, sample_event):
        content_ph = clear_placeholder(showcase_sidenav, "Page Content")
        add_plugin(
            content_ph,
            "SimpleTextPlugin",
            "en",
            position="last-child",
            text=(
                "This page demonstrates the Side Navigation plugin family (Side Navigation Child Page List, "
                "Side Navigation Page Link, and the Side Navigation Dynamic Filter placeholder) rendered "
                "in the page sidebar."
            ),
        )

        side_ph = clear_placeholder(showcase_sidenav, "Side Navigation")
        add_plugin(side_ph, "SideNavigationChildListPlugin", "en", position="last-child", show_second_level_children=True)
        add_plugin(
            side_ph,
            "SideNavigationPageLinkPlugin",
            "en",
            position="last-child",
            page=sample_event,
            text="Sample Event (manual link)",
        )
        add_plugin(side_ph, "SideNavigationDynamicFilterPlugin", "en", position="last-child")

    def _seed_showcase_people(self, showcase):
        people = [
            ("Fr. John Sullivan, C.S.C.", "Vice President for Mission Engagement and Church Affairs"),
            ("Dr. Maria Gonzalez", "Dean, College of Science"),
        ]
        for name, position in people:
            page = get_or_create_page(name, "person_page.html", parent=showcase, in_navigation=False)
            move_under_parent(page, showcase)
            set_preview_image(page, "profile1.jpg", alt=name)

            title_ph = page.get_placeholders("en").filter(slot="Person Title").first()
            if title_ph and not title_ph.get_plugins().filter(plugin_type="SimpleTextPlugin").exists():
                add_plugin(title_ph, "SimpleTextPlugin", "en", position="last-child", text=position)

            self.stdout.write(f"  Person page: {page.get_absolute_url()}")
