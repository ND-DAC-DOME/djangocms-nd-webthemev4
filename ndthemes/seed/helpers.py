from pathlib import Path

from django.core.files import File
from django.core.management.base import CommandError
from django.db import transaction

from cms.api import create_page
from cms.models import Page

from ndthemes.models import Event, EventSeries, PagePreviewExtension, PageTag, Setting

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "m4_demo" / "images"

FIXTURE_SPECS = {
    "campus1.jpg": (1200, 800, (12, 35, 64)),
    "campus3.jpg": (1200, 800, (174, 145, 66)),
    "profile1.jpg": (600, 600, (96, 96, 96)),
}


def ensure_fixture_images():
    """Create solid-color JPEG placeholders when demo images are missing."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise CommandError("Pillow is required to generate demo fixture images.") from exc

    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    for name, (width, height, color) in FIXTURE_SPECS.items():
        path = FIXTURES_DIR / name
        if path.exists():
            continue
        Image.new("RGB", (width, height), color).save(path, "JPEG", quality=85)


def fixture_path(name):
    ensure_fixture_images()
    path = FIXTURES_DIR / name
    if not path.exists():
        raise CommandError(f"Missing demo fixture image: {path}")
    return path


def page_by_title(title, language="en"):
    return Page.objects.filter(pagecontent_set__title=title, pagecontent_set__language=language).first()


def create_demo_page(title, template, parent=None, in_navigation=False):
    return create_page(
        title=title,
        template=template,
        language="en",
        in_navigation=in_navigation,
        parent=parent,
    )


def move_under_parent(page, parent):
    if page.parent_id != parent.pk:
        with transaction.atomic():
            page.move_page(parent, position="last-child")


def clear_placeholder(page, slot, language="en"):
    placeholder = page.get_placeholders(language).filter(slot=slot).first()
    if not placeholder:
        raise CommandError(f'Page "{page.get_page_title()}" has no "{slot}" placeholder.')
    for plugin in placeholder.get_plugins():
        plugin.delete()
    return placeholder


def save_plugin_image(plugin, field_name, image_name):
    with fixture_path(image_name).open("rb") as fh:
        getattr(plugin, field_name).save(image_name, File(fh), save=False)


def set_preview_image(page, image_name, alt="", summary="", publish_date=None):
    ext, _ = PagePreviewExtension.objects.get_or_create(extended_object=page)
    with fixture_path(image_name).open("rb") as fh:
        ext.image.save(image_name, File(fh), save=False)
    ext.image_alt = alt
    if summary:
        ext.summary_caption = summary
    if publish_date:
        ext.publish_date = publish_date
    ext.save()
    return ext


def tag_page(page, tag_name):
    tag, _ = PageTag.objects.get_or_create(tag=tag_name)
    ext, _ = PagePreviewExtension.objects.get_or_create(extended_object=page)
    ext.tags.add(tag)
    return ext


def ensure_page_tag(tag_name, *, search_category=False, archive_category=False):
    tag, _ = PageTag.objects.get_or_create(tag=tag_name)
    changed = False
    if tag.search_category != search_category:
        tag.search_category = search_category
        changed = True
    if tag.archive_category != archive_category:
        tag.archive_category = archive_category
        changed = True
    if changed:
        tag.save()
    return tag


def ensure_setting(key, setting_type="text", value="", enabled=False, page=None):
    setting, created = Setting.objects.get_or_create(
        key=key,
        defaults={"setting_type": setting_type, "value": value, "enabled": enabled, "page": page},
    )
    if not created:
        setting.setting_type = setting_type
        setting.value = value
        setting.enabled = enabled
        if page is not None:
            setting.page = page
        setting.save()
    return setting


def wipe_demo_site():
    """Remove CMS pages and domain records for a clean goirish run."""
    Event.objects.all().delete()
    EventSeries.objects.all().delete()
    Page.objects.all().delete()
