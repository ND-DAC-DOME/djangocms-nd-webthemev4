from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from cms.models import Page

from ndthemes.models import Setting
from ndthemes.seed.demo_content import (
    link_event_page_setting,
    seed_about_page,
    seed_archive_page,
    seed_events,
    seed_home,
    seed_news,
    seed_people,
)
from ndthemes.seed.helpers import (
    create_demo_page,
    ensure_fixture_images,
    ensure_page_tag,
    ensure_setting,
    page_by_title,
    wipe_demo_site,
)


class Command(BaseCommand):
    """Bootstrap a browsable demo site for ndthemes (M6 cookiecutter seed).

    Creates baseline settings/tags, a home page with NDT hero content, News/Events/People
    sections with sample content, About and Archive pages, and optional plugin showcases.
    """

    help = "Initialize demo settings, tags, pages, and sample content for ndthemes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete all CMS pages and domain records before seeding.",
        )
        parser.add_argument(
            "--separate",
            action="store_true",
            help="Create separate News and Events landing pages (default for M6).",
        )
        parser.add_argument(
            "--combined",
            action="store_true",
            help="Use a single combined News & Events landing page instead of separate pages.",
        )
        parser.add_argument(
            "--no-superuser",
            action="store_true",
            help="Skip the interactive createsuperuser prompt.",
        )
        parser.add_argument(
            "--demo-superuser",
            action="store_true",
            help="Create admin@example.com / changeme (skip interactive prompt).",
        )
        parser.add_argument(
            "--no-showcases",
            action="store_true",
            help="Skip plugin and component showcase pages.",
        )

    def handle(self, *args, **options):
        if options["combined"] and options["separate"]:
            self.stderr.write(self.style.ERROR("Use either --separate or --combined, not both."))
            return

        separate = options["separate"] or not options["combined"]

        if options["fresh"]:
            self.stdout.write("Clearing existing pages and domain records...")
            wipe_demo_site()

        ensure_fixture_images()
        self._ensure_settings()
        self._ensure_tags()

        if options["demo_superuser"]:
            self._ensure_demo_superuser()
        elif not options["no_superuser"]:
            self.stdout.write("Creating superuser (skip with --no-superuser or use --demo-superuser)...")
            call_command("createsuperuser")

        home = Page.objects.filter(is_home=True).first()
        if not home:
            self.stdout.write("Creating home page...")
            home = create_demo_page("Home", "home.html", in_navigation=True)
            with transaction.atomic():
                home.set_as_homepage()
        else:
            self.stdout.write("Home page exists; updating home content...")

        seed_home(home)

        events_page, news_page, people_page = self._ensure_landing_pages(home, separate)
        link_event_page_setting(events_page)

        news_tag = ensure_page_tag("News", search_category=True, archive_category=True)
        event_tag = ensure_page_tag("Event", search_category=True, archive_category=True)
        people_tag = ensure_page_tag("People", search_category=True, archive_category=True)

        self.stdout.write("Seeding news stories...")
        for story in seed_news(news_page, news_tag):
            self.stdout.write(f"  News: {story.get_absolute_url()}")

        self.stdout.write("Seeding events...")
        for event in seed_events(events_page, event_tag):
            self.stdout.write(f"  Event: {event.page.get_absolute_url()}")

        self.stdout.write("Seeding people pages...")
        for person in seed_people(people_page, people_tag):
            self.stdout.write(f"  Person: {person.get_absolute_url()}")

        about = seed_about_page(home, events_page)
        self.stdout.write(f"  About: {about.get_absolute_url()}")

        archive = seed_archive_page(home)
        self.stdout.write(f"  Archive: {archive.get_absolute_url()}")

        if not options["no_showcases"]:
            self.stdout.write("Seeding plugin and component showcases...")
            call_command("seed_plugin_showcase", no_people=False)
            call_command("seed_components_showcase")

        self.stdout.write(self.style.SUCCESS(f"Home: {home.get_absolute_url()}"))
        self.stdout.write(self.style.SUCCESS("Successfully initialized ndthemes demo site."))

    def _ensure_settings(self):
        self.stdout.write("Ensuring baseline settings...")
        defaults = [
            ("Site Name", "text", "ND Theme CMS", True),
            ("Site Description", "text", "Notre Dame django CMS base template (NDT 4.0).", True),
            ("Email", "text", "webhelp@nd.edu", True),
            ("Phone", "text", "(574) 631-5000", True),
            ("Address", "text", "Notre Dame, IN 46556 USA", True),
            ("Auto-archive events", "boolean", "", True),
            ("Event Page", "page", "", False),
        ]
        for key, setting_type, value, enabled in defaults:
            ensure_setting(key, setting_type=setting_type, value=value, enabled=enabled)

    def _ensure_tags(self):
        self.stdout.write("Ensuring baseline page tags...")
        ensure_page_tag("Event", search_category=True, archive_category=True)
        ensure_page_tag("News", search_category=True, archive_category=True)
        ensure_page_tag("People", search_category=True, archive_category=False)

    def _ensure_landing_pages(self, home, separate):
        events_page = page_by_title("Events")
        news_page = page_by_title("News")
        combined_page = page_by_title("News & Events")

        if separate:
            if not events_page:
                self.stdout.write("Creating Events landing page...")
                events_page = create_demo_page("Events", "event_listing.html", parent=home, in_navigation=True)
            if not news_page:
                self.stdout.write("Creating News landing page...")
                news_page = create_demo_page("News", "news_landing.html", parent=home, in_navigation=True)
        else:
            if not combined_page:
                self.stdout.write("Creating combined News & Events landing page...")
                combined_page = create_demo_page(
                    "News & Events",
                    "event_listing.html",
                    parent=home,
                    in_navigation=True,
                )
            events_page = combined_page
            news_page = combined_page

        people_page = page_by_title("People")
        if not people_page:
            self.stdout.write("Creating People landing page...")
            people_page = create_demo_page("People", "page_with_sidenav.html", parent=home, in_navigation=True)
        else:
            content = people_page.get_content_obj("en")
            if content.template != "page_with_sidenav.html":
                content.template = "page_with_sidenav.html"
                content.save()

        for landing_page in (events_page, news_page, people_page):
            if landing_page:
                move_under_parent(landing_page, home)

        return events_page, news_page, people_page

    def _ensure_demo_superuser(self):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser already exists, skipping demo account.")
            return
        User.objects.create_superuser("admin", "admin@example.com", "changeme")
        self.stdout.write(self.style.WARNING("Demo superuser: admin / changeme"))
