"""Demo page tree and sample content for goirish."""

from datetime import date, timedelta

from django.utils import timezone

from cms.api import add_plugin

from ndthemes.models import ChildPageList, Event, EventList, PersonListGrid, Setting

from .helpers import (
    clear_placeholder,
    create_demo_page,
    move_under_parent,
    page_by_title,
    save_plugin_image,
    set_preview_image,
    tag_page,
)


def seed_home(home):
    title_ph = home.get_placeholders("en").filter(slot="Page Title").first()
    if title_ph and not title_ph.get_plugins().exists():
        add_plugin(
            title_ph,
            "SimpleTextPlugin",
            "en",
            position="last-child",
            text="Welcome to ND Theme CMS",
        )

    lede_ph = home.get_placeholders("en").filter(slot="Page Lede").first()
    if lede_ph and not lede_ph.get_plugins().exists():
        add_plugin(
            lede_ph,
            "SimpleTextPlugin",
            "en",
            position="last-child",
            text="A django CMS 5 base template with Notre Dame Web Theme v4.",
        )

    intro_ph = home.get_placeholders("en").filter(slot="Page Intro").first()
    if intro_ph and not intro_ph.get_plugins().exists():
        add_plugin(
            intro_ph,
            "NDTNoticePlugin",
            "en",
            position="last-child",
            variant="info",
            heading="Sample site seeded by goirish",
            body=(
                "<p>This demo site includes News, Events, People, search, and NDT component "
                "plugins. Run <code>python manage.py goirish --fresh</code> to rebuild from scratch.</p>"
            ),
        )

    secondary_ph = home.get_placeholders("en").filter(slot="Page Secondary").first()
    if secondary_ph and not secondary_ph.get_plugins().filter(plugin_type="NDTBannerPlugin").exists():
        banner = add_plugin(
            secondary_ph,
            "NDTBannerPlugin",
            "en",
            position="last-child",
            layout="stacked",
            title="What would you fight for?",
            caption="<p>Notre Dame is a place where brilliant minds inspire each other to change the world.</p>",
            link_text="Explore Notre Dame",
            external_link="https://www.nd.edu",
        )
        save_plugin_image(banner, "image", "campus3.jpg")
        banner.save()

    content_ph = home.get_placeholders("en").filter(slot="Page Content").first()
    if content_ph and not content_ph.get_plugins().exists():
        add_plugin(
            content_ph,
            "NDTStatListPlugin",
            "en",
            position="last-child",
            columns="3",
        )
        stat_list = content_ph.get_plugins().filter(plugin_type="NDTStatListPlugin").first()
        for value, label, sticker in (
            ("1842", "Year founded", "library"),
            ("10%", "Acceptance rate", "grad-cap"),
            ("500+", "Student clubs", "football"),
        ):
            add_plugin(
                content_ph,
                "NDTStatPlugin",
                "en",
                target=stat_list,
                value=value,
                label=label,
                sticker=sticker,
            )


def seed_landing_page(page, slot, plugin_type, *, lede=None, **plugin_kwargs):
    lede_ph = page.get_placeholders("en").filter(slot="Page Lede").first()
    if lede_ph and lede and not lede_ph.get_plugins().exists():
        add_plugin(
            lede_ph,
            "SimpleTextPlugin",
            "en",
            position="last-child",
            text=lede,
        )

    list_ph = page.get_placeholders("en").filter(slot=slot).first()
    if not list_ph:
        return None
    existing = list_ph.get_plugins().filter(plugin_type=plugin_type).first()
    if existing:
        return existing
    return add_plugin(list_ph, plugin_type, "en", position="last-child", **plugin_kwargs)


def seed_news(news_page, news_tag):
    list_plugin = seed_landing_page(
        news_page,
        "News List",
        "ChildPageListPlugin",
        lede="Latest stories from across campus.",
        title="Latest news",
        parent_page=news_page,
        show_publication_date=True,
        order="date-desc",
    )
    if list_plugin:
        child_list = ChildPageList.objects.get(pk=list_plugin.pk)
        child_list.tags.add(news_tag)

    stories = (
        (
            "Notre Dame research discovers new method to address climate change",
            "campus3.jpg",
            "Research",
            date(2025, 4, 1),
            "Office of Public Affairs",
            "<p>Researchers at the University of Notre Dame have developed a new approach that could "
            "significantly reduce carbon emissions in industrial processes.</p>",
        ),
        (
            "Notre Dame researchers announce breakthrough in renewable energy storage",
            "campus1.jpg",
            "Science",
            date(2025, 1, 12),
            "Notre Dame Research",
            "<p>A multidisciplinary team has created a more efficient battery technology that could "
            "accelerate the transition to renewable energy.</p>",
        ),
        (
            "Campus community celebrates Founders Day",
            "campus1.jpg",
            "Campus life",
            date(2024, 11, 26),
            "Notre Dame News",
            "<p>Students, faculty, and staff gathered to honor the University's founding and its "
            "continuing mission in the Catholic intellectual tradition.</p>",
        ),
    )

    pages = []
    for title, image, category, published, author, body in stories:
        story = page_by_title(title)
        if not story:
            story = create_demo_page(title, "news_story.html", parent=news_page, in_navigation=False)
            move_under_parent(story, news_page)
        set_preview_image(story, image, alt=title, summary=f"{category} — {title[:80]}", publish_date=published)
        tag_page(story, "News")

        for slot, plugin_type, kwargs in (
            ("Publish Date", "SimpleTextPlugin", {"text": published.strftime("%B %d, %Y")}),
            ("Author", "SimpleTextPlugin", {"text": author}),
            ("Story Body", "TextPlugin", {"body": body}),
        ):
            ph = story.get_placeholders("en").filter(slot=slot).first()
            if ph and not ph.get_plugins().exists():
                add_plugin(ph, plugin_type, "en", position="last-child", **kwargs)
        pages.append(story)
    return pages


def seed_events(events_page, event_tag):
    list_plugin = seed_landing_page(
        events_page,
        "Events List",
        "EventListPlugin",
        lede="Upcoming lectures, workshops, and campus gatherings.",
        title="Upcoming events",
    )
    if list_plugin:
        event_list = EventList.objects.get(pk=list_plugin.pk)
        event_list.tags.add(event_tag)

    now = timezone.now()
    samples = (
        (
            "Faculty workshop on innovative teaching methods",
            now + timedelta(days=14, hours=10),
            now + timedelta(days=14, hours=12),
            "DeBartolo Hall, Room 101",
        ),
        (
            "Public lecture: Ethics and artificial intelligence",
            now + timedelta(days=28, hours=19),
            now + timedelta(days=28, hours=20, minutes=30),
            "Jordan Auditorium, Mendoza College of Business",
        ),
        (
            "Notre Dame Day celebration",
            now + timedelta(days=45, hours=16),
            now + timedelta(days=45, hours=20),
            "Main Quad",
        ),
    )

    events = []
    for name, start, end, location in samples:
        event = Event.objects.filter(name=name).first()
        if not event:
            event = Event(name=name, start=start, end=end, location=location)
            event.save()
        events.append(event)
    return events


def seed_storybook_pagination(content_ph):
    if content_ph.get_plugins().filter(plugin_type="NDTPaginationPlugin").exists():
        return
    pagination = add_plugin(content_ph, "NDTPaginationPlugin", "en", position="last-child")
    add_plugin(
        content_ph,
        "NDTPaginationItemPlugin",
        "en",
        target=pagination,
        label="Previous",
        item_type="disabled",
    )
    for page_num in ("1", "2", "3", "4", "5"):
        add_plugin(
            content_ph,
            "NDTPaginationItemPlugin",
            "en",
            target=pagination,
            label=page_num,
            item_type="current" if page_num == "1" else "page",
            external_link="#",
        )
    add_plugin(
        content_ph,
        "NDTPaginationItemPlugin",
        "en",
        target=pagination,
        label="Next",
        item_type="next",
        external_link="#",
    )


def seed_people(people_page, people_tag):
    content_ph = people_page.get_placeholders("en").filter(slot="Page Content").first()
    if content_ph and not content_ph.get_plugins().filter(plugin_type="TextPlugin").exists():
        add_plugin(
            content_ph,
            "TextPlugin",
            "en",
            position="first-child",
            body=(
                "<p>This is an example of a people listing page. It features a selection of "
                "staff members displayed in a list or grid format. Each profile includes a name, "
                "title, summary, and link to their full profile.</p>"
            ),
        )

    if content_ph and not content_ph.get_plugins().filter(plugin_type="PersonGridListPlugin").exists():
        grid_plugin = add_plugin(
            content_ph,
            "PersonGridListPlugin",
            "en",
            position="last-child",
        )
        grid = PersonListGrid.objects.get(pk=grid_plugin.pk)
        grid.tags.add(people_tag)

    seed_storybook_pagination(content_ph)

    side_ph = people_page.get_placeholders("en").filter(slot="Side Navigation").first()
    if side_ph and not side_ph.get_plugins().filter(plugin_type="SideNavigationChildListPlugin").exists():
        for plugin in list(side_ph.get_plugins()):
            plugin.delete()
        add_plugin(
            side_ph,
            "SideNavigationChildListPlugin",
            "en",
            position="last-child",
            show_second_level_children=False,
        )

    people = (
        (
            "Rev. Robert A. Dowd, C.S.C.",
            "President of the University of Notre Dame",
            "profile1.jpg",
            "574-631-5000",
            "president@nd.edu",
            "Main Building",
            "<p>Rev. Robert A. Dowd, C.S.C., serves as the 18th president of the University of Notre Dame.</p>",
        ),
        (
            "Jane Doe",
            "Professor of Theology",
            "profile1.jpg",
            "574-631-1234",
            "jane.doe@nd.edu",
            "Geddes Hall",
            "<p>Jane Doe researches Catholic social teaching and its application to contemporary policy debates.</p>",
        ),
        (
            "John Smith",
            "Director of Notre Dame Research",
            "profile1.jpg",
            "574-631-5678",
            "john.smith@nd.edu",
            "Hesburgh Library",
            "<p>John Smith leads interdisciplinary research initiatives across the University.</p>",
        ),
    )

    pages = []
    for name, position, image, phone, email, office, bio in people:
        person = page_by_title(name)
        if not person:
            person = create_demo_page(name, "person_page.html", parent=people_page, in_navigation=False)
            move_under_parent(person, people_page)
        set_preview_image(person, image, alt=name, summary=position)
        tag_page(person, "People")

        fields = (
            ("Person Title", "SimpleTextPlugin", {"text": position}),
            ("Address", "SimpleTextPlugin", {"text": office}),
            ("Phone", "PhoneNumberPlugin", {"phone_number": phone}),
            ("Email", "EmailLinkPlugin", {"text": email, "email": email}),
            ("About", "TextPlugin", {"body": bio}),
        )
        for slot, plugin_type, kwargs in fields:
            ph = person.get_placeholders("en").filter(slot=slot).first()
            if ph and not ph.get_plugins().exists():
                add_plugin(ph, plugin_type, "en", position="last-child", **kwargs)

        profile_ph = person.get_placeholders("en").filter(slot="Profile Picture").first()
        if profile_ph and not profile_ph.get_plugins().exists():
            image_plugin = add_plugin(
                profile_ph,
                "NDTImageSinglePlugin",
                "en",
                position="last-child",
                alt_text=name,
                layout="circle",
            )
            save_plugin_image(image_plugin, "image", image)
            image_plugin.save()
        pages.append(person)
    return pages


def seed_about_page(home, events_page):
    about = page_by_title("About")
    if not about:
        about = create_demo_page("About", "page_with_sidenav.html", parent=home, in_navigation=True)
    move_under_parent(about, home)

    content_ph = about.get_placeholders("en").filter(slot="Page Content").first()
    if content_ph and content_ph.get_plugins().exists():
        return about

    content_ph = clear_placeholder(about, "Page Content")
    add_plugin(
        content_ph,
        "NDTHeadingPlugin",
        "en",
        position="last-child",
        level="2",
        text="About this demo site",
        css_class="section-title",
    )
    add_plugin(
        content_ph,
        "NDTAccordionPlugin",
        "en",
        position="last-child",
    )
    accordion = content_ph.get_plugins().filter(plugin_type="NDTAccordionPlugin").first()
    for title, body in (
        ("What is goirish?", "<p>goirish bootstraps settings, tags, and a browsable sample page tree for local development.</p>"),
        ("How do I reset?", "<p>Run <code>docker compose -f local.yml down -v</code>, then migrate and goirish again.</p>"),
    ):
        item = add_plugin(
            content_ph,
            "NDTAccordionItemPlugin",
            "en",
            target=accordion,
            title=title,
            open_by_default=title.startswith("What"),
        )
        add_plugin(content_ph, "SimpleTextPlugin", "en", target=item, text=body)

    side_ph = about.get_placeholders("en").filter(slot="Side Navigation").first()
    if side_ph and not side_ph.get_plugins().exists():
        add_plugin(side_ph, "SideNavigationChildListPlugin", "en", position="last-child", show_second_level_children=True)
        add_plugin(
            side_ph,
            "SideNavigationPageLinkPlugin",
            "en",
            position="last-child",
            page=events_page,
            text="Upcoming events",
        )
    return about


def seed_archive_page(home):
    archive = page_by_title("Archive")
    if not archive:
        archive = create_demo_page("Archive", "archive_results.html", parent=home, in_navigation=True)
    move_under_parent(archive, home)

    lede_ph = archive.get_placeholders("en").filter(slot="Page Lede").first()
    if lede_ph and not lede_ph.get_plugins().exists():
        add_plugin(
            lede_ph,
            "SimpleTextPlugin",
            "en",
            position="last-child",
            text="Browse archived news and events.",
        )

    results_ph = archive.get_placeholders("en").filter(slot="Archive Results").first()
    if results_ph and not results_ph.get_plugins().exists():
        add_plugin(
            results_ph,
            "ArchiveLinkPlugin",
            "en",
            position="last-child",
            text="View the full archive",
        )
    return archive


def link_event_page_setting(events_page):
    setting = Setting.objects.get(key="Event Page")
    setting.page = events_page
    setting.save()
