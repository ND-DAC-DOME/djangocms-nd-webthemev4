"""
Seed M5 NDT component showcase page.

Builds a review page exercising the first batch of ndthemes/components plugins.
Safe to re-run: the showcase placeholder is cleared and rebuilt each time.

Usage:
    python manage.py seed_components_showcase
"""
from pathlib import Path
from datetime import date, time

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cms.api import add_plugin, create_page
from cms.models import Page

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
    help = "Seed Component Showcase page for M5 NDT component plugin QA."

    def handle(self, *args, **options):
        home = Page.objects.filter(is_home=True).first()
        if not home:
            raise CommandError("No home page found. Run `python manage.py goirish` first.")

        self.stdout.write("Building Component Showcase page...")
        showcase = page_by_title("Component Showcase")
        if not showcase:
            showcase = create_page(
                title="Component Showcase",
                template="page.html",
                language="en",
                in_navigation=False,
            )
        move_under_parent(showcase, home)
        self._seed_showcase(showcase)
        self.stdout.write(self.style.SUCCESS(f"  {showcase.get_absolute_url()}"))
        self.stdout.write(self.style.SUCCESS("Component showcase seed complete."))

    def _seed_showcase(self, page):
        placeholder = clear_placeholder(page, "Page Content")

        add_plugin(
            placeholder,
            "NDTHeadingPlugin",
            "en",
            position="last-child",
            level="1",
            text="NDT Component Showcase",
            css_class="section-title",
        )

        add_plugin(
            placeholder,
            "NDTNoticePlugin",
            "en",
            position="last-child",
            variant="info",
            heading="M5 component plugins",
            body="<p>Native NDT4 Storybook component plugins for local QA.</p>",
        )

        accordion = add_plugin(
            placeholder,
            "NDTAccordionPlugin",
            "en",
            position="last-child",
            size="lg",
            style="highlight",
        )
        item_one = add_plugin(
            placeholder,
            "NDTAccordionItemPlugin",
            "en",
            target=accordion,
            title="What is this page?",
            open_by_default=True,
        )
        add_plugin(
            placeholder,
            "SimpleTextPlugin",
            "en",
            target=item_one,
            text="This page exercises M5 ndthemes/components plugins with native NDT4 markup.",
        )
        item_two = add_plugin(
            placeholder,
            "NDTAccordionItemPlugin",
            "en",
            target=accordion,
            title="How do I re-seed?",
        )
        add_plugin(
            placeholder,
            "SimpleTextPlugin",
            "en",
            target=item_two,
            text="Run `python manage.py seed_components_showcase` to rebuild this page.",
        )

        add_plugin(
            placeholder,
            "NDTQuotePlugin",
            "en",
            position="last-child",
            quote="<p>Education is the most powerful weapon which you can use to change the world.</p>",
            citation="Nelson Mandela",
            size="lg",
            alignment="centered",
        )

        stat_list = add_plugin(
            placeholder,
            "NDTStatListPlugin",
            "en",
            position="last-child",
            columns="3",
        )
        stats = (
            ("500+", "Student Clubs and Groups", "grad-cap"),
            ("28", "Campus Eateries", ""),
            ("10%", "Acceptance Rate", ""),
        )
        for value, label, sticker in stats:
            add_plugin(
                placeholder,
                "NDTStatPlugin",
                "en",
                target=stat_list,
                value=value,
                label=label,
                sticker=sticker,
            )

        tabs = add_plugin(
            placeholder,
            "NDTTabsPlugin",
            "en",
            position="last-child",
        )
        tab_one = add_plugin(
            placeholder,
            "NDTTabPanelPlugin",
            "en",
            target=tabs,
            title="Overview",
            active_by_default=True,
        )
        add_plugin(
            placeholder,
            "SimpleTextPlugin",
            "en",
            target=tab_one,
            text="Tabs use native NDT4 nav-tabs / tab-panel markup with site.js interaction.",
        )
        tab_two = add_plugin(
            placeholder,
            "NDTTabPanelPlugin",
            "en",
            target=tabs,
            title="Lists & tables",
        )
        add_plugin(
            placeholder,
            "SimpleTextPlugin",
            "en",
            target=tab_two,
            text="This tab sits alongside list, table, and timeline examples below.",
        )

        stepped_list = add_plugin(
            placeholder,
            "NDTListPlugin",
            "en",
            position="last-child",
            list_type="stepped",
            label="Stepped list",
        )
        for title, body in (
            ("Apply", "<p>Submit your application during the open window.</p>"),
            ("Review", "<p>Admissions reviews materials holistically.</p>"),
            ("Decision", "<p>Applicants receive notification by the posted date.</p>"),
        ):
            add_plugin(
                placeholder,
                "NDTListItemPlugin",
                "en",
                target=stepped_list,
                title=title,
                body=body,
            )

        add_plugin(
            placeholder,
            "NDTTablePlugin",
            "en",
            position="last-child",
            caption="Sample course table",
            body=(
                "<thead><tr><th>Course</th><th>Credits</th><th>Term</th></tr></thead>"
                "<tbody>"
                "<tr><td>Introduction to Theology</td><td>3</td><td>Fall</td></tr>"
                "<tr><td>Calculus I</td><td>4</td><td>Fall</td></tr>"
                "<tr><td>Writing & Rhetoric</td><td>3</td><td>Spring</td></tr>"
                "</tbody>"
            ),
        )

        timeline = add_plugin(
            placeholder,
            "NDTTimelinePlugin",
            "en",
            position="last-child",
        )
        for title, when, body in (
            (
                "Campus founded",
                "1842",
                "<p>Rev. Edward Sorin, C.S.C., and companions arrive at Notre Dame.</p>",
            ),
            (
                "Golden Dome completed",
                "1882",
                "<p>The Main Building dome becomes a campus landmark.</p>",
            ),
            (
                "Continued mission",
                "Today",
                "<p>The University pursues research and formation in the Catholic tradition.</p>",
            ),
        ):
            add_plugin(
                placeholder,
                "NDTTimelineItemPlugin",
                "en",
                target=timeline,
                title=title,
                date=when,
                body=body,
            )

        add_plugin(
            placeholder,
            "NDTHeadingPlugin",
            "en",
            position="last-child",
            level="2",
            text="Media components",
            css_class="section-title",
        )

        image_single = add_plugin(
            placeholder,
            "NDTImageSinglePlugin",
            "en",
            position="last-child",
            alt_text="Campus image",
            caption="Image (single), default layout.",
            layout="",
        )
        save_plugin_image(image_single, "image", "campus1.jpg")
        image_single.save()

        image_multiple = add_plugin(
            placeholder,
            "NDTImageMultiplePlugin",
            "en",
            position="last-child",
            layout="tiled",
        )
        for idx, image_name in enumerate(("campus1.jpg", "campus3.jpg", "profile1.jpg"), start=1):
            item = add_plugin(
                placeholder,
                "NDTImageMultipleItemPlugin",
                "en",
                target=image_multiple,
                alt_text=f"Campus image {idx}",
            )
            save_plugin_image(item, "image", image_name)
            item.save()

        gallery = add_plugin(placeholder, "NDTGalleryPlugin", "en", position="last-child")
        for idx, image_name in enumerate(("campus1.jpg", "campus3.jpg", "profile1.jpg"), start=1):
            item = add_plugin(
                placeholder,
                "NDTGalleryItemPlugin",
                "en",
                target=gallery,
                title=f"Gallery image {idx}",
                alt_text=f"Gallery image {idx}",
            )
            save_plugin_image(item, "image", image_name)
            item.save()

        add_plugin(
            placeholder,
            "NDTVideoPlugin",
            "en",
            position="last-child",
            display_type="embed",
            video_url="https://www.youtube.com/watch?v=p_vC10eq474",
            label="Welcome to the Notre Dame family",
        )

        avatar = add_plugin(
            placeholder,
            "NDTAvatarPlugin",
            "en",
            position="last-child",
            alt_text="University president portrait",
            caption="Rev. Robert A. Dowd, C.S.C.",
            size="md",
        )
        save_plugin_image(avatar, "image", "profile1.jpg")
        avatar.save()

        add_plugin(
            placeholder,
            "NDTHeadingPlugin",
            "en",
            position="last-child",
            level="2",
            text="Buttons & navigation",
            css_class="section-title",
        )

        home = Page.objects.filter(is_home=True).first()
        btn_group = add_plugin(placeholder, "NDTButtonGroupPlugin", "en", position="last-child")
        for idx, text in enumerate(("Overview", "Academics", "Research", "About"), start=1):
            add_plugin(
                placeholder,
                "NDTButtonItemPlugin",
                "en",
                target=btn_group,
                text=text,
                active=(idx == 1),
                link=home,
            )

        btn_list = add_plugin(placeholder, "NDTButtonListPlugin", "en", position="last-child")
        for text in ("Undergraduate Admissions", "Graduate Programs", "Visit Campus"):
            add_plugin(
                placeholder,
                "NDTButtonItemPlugin",
                "en",
                target=btn_list,
                text=text,
                external_link="https://www.nd.edu",
            )

        add_plugin(
            placeholder,
            "NDTIconButtonPlugin",
            "en",
            position="last-child",
            text="Explore Notre Dame",
            icon="arrow-right",
            alignment="right",
            external_link="https://www.nd.edu",
        )

        add_plugin(
            placeholder,
            "NDTLedeButtonPlugin",
            "en",
            position="last-child",
            text="Notre Dame attracts brilliant, energetic thinkers who are motivated to change the world.",
            external_link="https://www.nd.edu",
        )

        nav_anchor = add_plugin(
            placeholder,
            "NDTNavAnchorPlugin",
            "en",
            position="last-child",
            label="On this page",
        )
        for idx, text in enumerate(("Academics", "Admissions", "Research"), start=1):
            add_plugin(
                placeholder,
                "NDTNavAnchorItemPlugin",
                "en",
                target=nav_anchor,
                text=text,
                external_link=f"#section-{idx}",
                active=(idx == 1),
            )

        pagination = add_plugin(placeholder, "NDTPaginationPlugin", "en", position="last-child")
        add_plugin(
            placeholder,
            "NDTPaginationItemPlugin",
            "en",
            target=pagination,
            label="Previous",
            item_type="previous",
            external_link="#",
        )
        for page_num in ("1", "2", "3"):
            add_plugin(
                placeholder,
                "NDTPaginationItemPlugin",
                "en",
                target=pagination,
                label=page_num,
                item_type="current" if page_num == "2" else "page",
                external_link="#",
            )
        add_plugin(
            placeholder,
            "NDTPaginationItemPlugin",
            "en",
            target=pagination,
            label="Next",
            item_type="next",
            external_link="#",
        )

        add_plugin(
            placeholder,
            "NDTHeadingPlugin",
            "en",
            position="last-child",
            level="2",
            text="Cards",
            css_class="section-title",
        )

        card_list = add_plugin(placeholder, "NDTCardListPlugin", "en", position="last-child")

        default_card = add_plugin(
            placeholder,
            "NDTCardDefaultPlugin",
            "en",
            target=card_list,
            title="Explore campus life",
            summary="<p>Hendrerit in quis venenatis aliquet venenatis scelerisque in ipsum parturient congue vulputate convallis ultricies at.</p>",
            external_link="https://www.nd.edu",
        )
        save_plugin_image(default_card, "image", "campus1.jpg")
        default_card.save()

        news_card = add_plugin(
            placeholder,
            "NDTCardNewsPlugin",
            "en",
            target=card_list,
            label="Research",
            title="Notre Dame research discovers new method to address climate change",
            author_name="Jane Smith",
            publish_date=date(2025, 4, 1),
            external_link="https://www.nd.edu",
        )
        save_plugin_image(news_card, "image", "campus3.jpg")
        news_card.save()

        add_plugin(
            placeholder,
            "NDTCardEventPlugin",
            "en",
            target=card_list,
            title="Faculty workshop on innovative teaching methods",
            description="Join us for an interactive workshop on teaching methods.",
            event_date=date(2025, 4, 15),
            start_time=time(10, 0),
            end_time=time(12, 0),
            location="DeBartolo Hall, Room 101",
            external_link="https://www.nd.edu",
        )

        featured_card = add_plugin(
            placeholder,
            "NDTCardFeaturedPlugin",
            "en",
            target=card_list,
            label="Featured",
            title="Fight for the future",
            external_link="https://www.nd.edu",
        )
        save_plugin_image(featured_card, "image", "campus1.jpg")
        featured_card.save()

        person_card = add_plugin(
            placeholder,
            "NDTCardPersonPlugin",
            "en",
            target=card_list,
            title="John Doe",
            job_title="Professor of Theology",
            summary="<p>Hendrerit in quis venenatis aliquet venenatis scelerisque in ipsum parturient congue vulputate convallis ultricies at.</p>",
            external_link="https://www.nd.edu",
        )
        save_plugin_image(person_card, "image", "profile1.jpg")
        person_card.save()

        media_mention = add_plugin(
            placeholder,
            "NDTCardMediaMentionPlugin",
            "en",
            position="last-child",
            publication_name="National Public Radio",
            publication_slug="npr",
            title="Notre Dame researchers find breakthrough in renewable energy storage",
            mention_date="January 12, 2025",
            summary="<p>Researchers at the University of Notre Dame have developed a new approach to energy storage.</p>",
            external_link="https://www.nd.edu",
        )
        byline = add_plugin(
            placeholder,
            "NDTCardBylineItemPlugin",
            "en",
            target=media_mention,
            name="John Smith",
            title="College of Arts and Letters",
            external_link="https://www.nd.edu",
        )
        save_plugin_image(byline, "image", "profile1.jpg")
        byline.save()

        media_quoted = add_plugin(
            placeholder,
            "NDTCardMediaMentionQuotedPlugin",
            "en",
            position="last-child",
            publication_name="New York Times",
            publication_slug="nyt",
            quote="<p>“People are legitimately actually pissed off at the health care industry and the way it operates.”</p>",
            link_text="Read article",
            external_link="https://www.nd.edu",
        )
        add_plugin(
            placeholder,
            "NDTCardBylineItemPlugin",
            "en",
            target=media_quoted,
            name="Tim Weninger",
            title="in New York Times",
            external_link="https://www.nd.edu",
        )

        footnotes = add_plugin(placeholder, "NDTFootnoteListPlugin", "en", position="last-child")
        for body in (
            "University of Notre Dame, “About Notre Dame,” <a href=\"https://www.nd.edu/about/\">https://www.nd.edu/about/</a>.",
            "Notre Dame Archives, “A Brief History,” <a href=\"https://archives.nd.edu/history.htm\">https://archives.nd.edu/history.htm</a>.",
        ):
            add_plugin(
                placeholder,
                "NDTFootnoteItemPlugin",
                "en",
                target=footnotes,
                body=f"<p>{body}</p>",
            )

        add_plugin(
            placeholder,
            "NDTDialogPlugin",
            "en",
            position="last-child",
            trigger_text="Open dialog",
            heading="Dialog title",
            body="<p>This dialog uses native NDT4 markup. Click outside or use the close button to dismiss.</p>",
            footer="Supporting text or action buttons can go in the footer.",
        )

        faq = add_plugin(
            placeholder,
            "NDTFAQPlugin",
            "en",
            position="last-child",
            show_anchors=True,
            anchors_id="faq-showcase",
            show_back_to_top=True,
        )
        for idx, (question, answer) in enumerate(
            (
                (
                    "What is the history behind the Golden Dome?",
                    "The Golden Dome is the main building at Notre Dame and one of the most recognizable university landmarks in the world.",
                ),
                (
                    "How competitive is admission to Notre Dame?",
                    "Notre Dame is highly selective, with an acceptance rate typically between 15–18%.",
                ),
            ),
            start=1,
        ):
            add_plugin(
                placeholder,
                "NDTFAQItemPlugin",
                "en",
                target=faq,
                item_id=f"faq_{idx:03d}",
                question=question,
                answer=f"<p>{answer}</p>",
            )

        banner = add_plugin(
            placeholder,
            "NDTBannerPlugin",
            "en",
            position="last-child",
            layout="stacked",
            title="Banner (stacked)",
            caption="<p>Risus parturient ullamcorper luctus tempor nisl lacus nec sociis cras a vestibulum.</p>",
            external_link="#",
            link_text="Explore all programs",
        )
        save_plugin_image(banner, "image", "campus3.jpg")
        banner.save()

        page_header = add_plugin(
            placeholder,
            "NDTPageHeaderPlugin",
            "en",
            position="last-child",
            title="Do more than dream about the future. Fight for it.",
            lede="Example page lede providing additional context about the page.",
            title_size="sm",
        )
        save_plugin_image(page_header, "image", "campus3.jpg")
        page_header.save()

        add_plugin(
            placeholder,
            "NDTHeadingPlugin",
            "en",
            position="last-child",
            level="2",
            text="Utilities & forms",
            css_class="section-title",
        )

        add_plugin(
            placeholder,
            "NDTButtonPlugin",
            "en",
            position="last-child",
            text="Standalone button",
            style="cta",
            external_link="https://www.nd.edu",
        )

        byline = add_plugin(
            placeholder,
            "NDTBylinePlugin",
            "en",
            position="last-child",
            name="Rev. Robert A. Dowd, C.S.C.",
            title="President of the University of Notre Dame",
            external_link="#",
        )
        save_plugin_image(byline, "image", "profile1.jpg")
        byline.save()

        add_plugin(placeholder, "NDTSocialSharePlugin", "en", position="last-child")

        add_plugin(
            placeholder,
            "NDTVideoButtonPlugin",
            "en",
            position="last-child",
            text="View video",
            style="ornamental",
            external_link="#video",
        )

        add_plugin(
            placeholder,
            "NDTIconPlugin",
            "en",
            position="last-child",
            icon="search",
            size="lg",
            label="Search icon",
        )

        add_plugin(
            placeholder,
            "NDTStickerPlugin",
            "en",
            position="last-child",
            sticker="grad-cap",
            size="md",
            label="Grad cap sticker",
        )

        stacked_quote = add_plugin(
            placeholder,
            "NDTQuotePlugin",
            "en",
            position="last-child",
            layout="stacked",
            variant="primary",
            quote="<p>Education is the most powerful weapon which you can use to change the world.</p>",
            author_name="Nelson Mandela",
            author_title="Human rights activist",
        )
        save_plugin_image(stacked_quote, "author_image", "profile1.jpg")
        stacked_quote.save()

        mosaic_banner = add_plugin(
            placeholder,
            "NDTBannerPlugin",
            "en",
            position="last-child",
            layout="mosaic",
            title="Banner (mosaic)",
            caption="<p>Mosaic image layout with multiple banner images.</p>",
            intro_alignment="text-left",
            external_link="#",
        )
        for image_name in ("campus1.jpg", "campus3.jpg"):
            item = add_plugin(
                placeholder,
                "NDTBannerImageItemPlugin",
                "en",
                target=mosaic_banner,
            )
            save_plugin_image(item, "image", image_name)
            item.save()

        contact_form = add_plugin(
            placeholder,
            "NDTFormPlugin",
            "en",
            position="last-child",
            title="Contact us",
            submit_label="Send message",
        )
        add_plugin(
            placeholder,
            "NDTFormFieldPlugin",
            "en",
            target=contact_form,
            label="First name",
            field_type="text",
            field_id="first-name",
            input_placeholder="Jane",
            required=True,
        )
        add_plugin(
            placeholder,
            "NDTFormFieldPlugin",
            "en",
            target=contact_form,
            label="Email",
            field_type="email",
            field_id="email",
            input_placeholder="jane@example.com",
            required=True,
        )
        add_plugin(
            placeholder,
            "NDTFormFieldPlugin",
            "en",
            target=contact_form,
            label="Message",
            field_type="textarea",
            field_id="message",
            input_placeholder="How can we help?",
        )

        add_plugin(
            placeholder,
            "NDTSearchFormPlugin",
            "en",
            position="last-child",
            label="Search this site",
            input_placeholder="Search…",
            action="/search/",
        )

        add_plugin(
            placeholder,
            "NDTNoticePlugin",
            "en",
            position="last-child",
            variant="success",
            heading="M5 component library complete",
            body="<p>All stable NDT4 Storybook component families are available as native CMS plugins.</p>",
        )
