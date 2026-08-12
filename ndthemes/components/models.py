from django.db import models

from cms.models.fields import PageField
from cms.models.pluginmodel import CMSPlugin
from djangocms_text.fields import HTMLField


STICKER_CHOICES = (
    ("backpack", "Backpack"),
    ("chalk-board", "Chalk board"),
    ("dna", "DNA"),
    ("football", "Football"),
    ("globe", "Globe"),
    ("grad-cap", "Grad cap"),
    ("library", "Library"),
    ("microscope", "Microscope"),
)


class Accordion(CMSPlugin):
    SIZE_CHOICES = (
        ("", "Default"),
        ("sm", "Small"),
        ("lg", "Large"),
    )
    STYLE_CHOICES = (
        ("", "Default"),
        ("highlight", "Highlighted"),
        ("bg", "With background"),
    )

    size = models.CharField(max_length=16, choices=SIZE_CHOICES, blank=True, default="")
    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")

    def __str__(self):
        return "Accordion"

    def accordion_class(self):
        classes = ["accordion"]
        if self.size:
            classes.append(f"accordion--{self.size}")
        if self.style:
            classes.append(f"accordion--{self.style}")
        return " ".join(classes)


class AccordionItem(CMSPlugin):
    title = models.CharField(max_length=255)
    open_by_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def search_fields(self):
        return ("title",)


class Notice(CMSPlugin):
    VARIANT_CHOICES = (
        ("", "Default"),
        ("primary", "Primary"),
        ("secondary", "Secondary"),
        ("success", "Success"),
        ("info", "Info"),
        ("warning", "Warning"),
        ("danger", "Danger"),
    )

    variant = models.CharField(max_length=16, choices=VARIANT_CHOICES, blank=True, default="")
    heading = models.CharField(max_length=255, blank=True, default="")
    body = HTMLField(blank=True, default="")

    def __str__(self):
        return self.heading or "Notice"

    @property
    def search_fields(self):
        return ("heading", "body")

    def notice_class(self):
        if self.variant:
            return f"notice notice--{self.variant}"
        return "notice"


class Heading(CMSPlugin):
    LEVEL_CHOICES = tuple((str(n), f"Heading {n}") for n in range(1, 7))

    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default="2")
    text = models.CharField(max_length=512)
    css_class = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Optional extra classes (e.g. section-title).",
    )

    def __str__(self):
        return self.text

    @property
    def search_fields(self):
        return ("text",)


class Quote(CMSPlugin):
    LAYOUT_CHOICES = (
        ("default", "Default"),
        ("inline", "Inline"),
        ("stacked", "Stacked"),
    )
    SIZE_CHOICES = (
        ("sm", "Small"),
        ("md", "Medium"),
        ("lg", "Large"),
        ("xl", "Extra large"),
    )
    VARIANT_CHOICES = (
        ("", "Default"),
        ("primary", "Primary"),
    )
    ALIGN_CHOICES = (
        ("", "Default"),
        ("centered", "Centered"),
        ("right", "Right"),
        ("reversed", "Reversed"),
    )

    layout = models.CharField(max_length=16, choices=LAYOUT_CHOICES, default="default")
    quote = HTMLField()
    citation = models.CharField(max_length=512, blank=True, default="")
    author_name = models.CharField(max_length=255, blank=True, default="")
    author_title = models.CharField(max_length=255, blank=True, default="")
    author_image = models.ImageField(upload_to="ndthemes/quotes/", blank=True, null=True)
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, default="md")
    variant = models.CharField(max_length=16, choices=VARIANT_CHOICES, blank=True, default="")
    alignment = models.CharField(max_length=16, choices=ALIGN_CHOICES, blank=True, default="")

    def __str__(self):
        return self.author_name or self.citation or "Quote"

    @property
    def search_fields(self):
        return ("quote", "citation", "author_name", "author_title")

    def blockquote_class(self):
        classes = ["blockquote"]
        if self.layout == "default" and self.size:
            classes.append(f"blockquote--{self.size}")
        if self.variant:
            classes.append(f"blockquote--{self.variant}")
        if self.alignment:
            classes.append(f"blockquote--{self.alignment}")
        return " ".join(classes)


class Stat(CMSPlugin):
    SIZE_CHOICES = (
        ("xs", "Extra small"),
        ("sm", "Small"),
        ("md", "Medium"),
        ("lg", "Large"),
    )

    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, default="md")
    centered = models.BooleanField(default=False)
    sticker = models.CharField(max_length=32, choices=STICKER_CHOICES, blank=True, default="")
    sticker_size = models.CharField(
        max_length=8,
        choices=(("", "Default"), ("sm", "Small"), ("lg", "Large"), ("xl", "Extra large")),
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.value} — {self.label}"

    def stat_sticker_class(self):
        classes = ["stat-sticker"]
        if self.sticker_size:
            classes.append(f"sticker--{self.sticker_size}")
        return " ".join(classes)


class StatList(CMSPlugin):
    COLUMN_CHOICES = (
        ("2", "2 columns"),
        ("3", "3 columns"),
        ("4", "4 columns"),
    )

    columns = models.CharField(max_length=1, choices=COLUMN_CHOICES, default="3")

    def __str__(self):
        return f"Stat list ({self.columns} columns)"

    def list_class(self):
        return f"no-bullets list--stats grid grid-sm-{self.columns}"


class Tabs(CMSPlugin):
    SIZE_CHOICES = (
        ("", "Default"),
        ("lg", "Large"),
    )

    size = models.CharField(max_length=8, choices=SIZE_CHOICES, blank=True, default="")

    def __str__(self):
        return "Tabs"

    def nav_class(self):
        classes = ["nav-tabs"]
        if self.size:
            classes.append(f"nav-tabs--{self.size}")
        return " ".join(classes)


class TabPanel(CMSPlugin):
    title = models.CharField(max_length=255)
    active_by_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class List(CMSPlugin):
    TYPE_CHOICES = (
        ("unordered", "Unordered"),
        ("ordered", "Ordered"),
        ("unstyled", "Unstyled"),
        ("inline", "Inline"),
        ("stepped", "Stepped"),
        ("spaced", "Spaced"),
    )

    list_type = models.CharField(max_length=16, choices=TYPE_CHOICES, default="unordered")
    label = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Optional label shown above the list.",
    )

    def __str__(self):
        return f"List ({self.get_list_type_display()})"

    def tag_name(self):
        if self.list_type in ("ordered", "stepped"):
            return "ol"
        return "ul"

    def list_class(self):
        classes = {
            "unstyled": "list--unstyled",
            "inline": "list--inline",
            "stepped": "ol--stepped",
            "spaced": "list--spaced",
        }
        return classes.get(self.list_type, "")


class ListItem(CMSPlugin):
    title = models.CharField(max_length=255, blank=True, default="")
    body = HTMLField(blank=True, default="")

    def __str__(self):
        return self.title or "List item"


class Table(CMSPlugin):
    STYLE_CHOICES = (
        ("", "Default"),
        ("minimal", "Minimal"),
    )

    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")
    caption = models.CharField(max_length=255, blank=True, default="")
    body = HTMLField(
        help_text="Table markup without the outer <table> tag (use thead/tbody rows).",
    )

    def __str__(self):
        return self.caption or "Table"

    def table_class(self):
        if self.style:
            return f"table--{self.style}"
        return ""


class Timeline(CMSPlugin):
    ALIGNMENT_CHOICES = (
        ("", "Default"),
        ("right", "Right"),
        ("center", "Center"),
    )

    alignment = models.CharField(max_length=16, choices=ALIGNMENT_CHOICES, blank=True, default="")

    def __str__(self):
        return "Timeline"

    def timeline_class(self):
        if self.alignment:
            return f"timeline timeline--{self.alignment}"
        return "timeline"


class TimelineItem(CMSPlugin):
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=128, blank=True, default="")
    body = HTMLField(blank=True, default="")
    image = models.ImageField(blank=True, null=True, upload_to="ndthemes/timeline/")
    image_alt = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.title


class Gallery(CMSPlugin):
    STYLE_CHOICES = (
        ("", "Default grid"),
        ("tiled", "Tiled"),
        ("tiled-alt", "Tiled (alternate)"),
        ("slider", "Slider"),
    )

    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")

    def __str__(self):
        return "Gallery"

    def gallery_class(self):
        classes = ["gallery-lb", f"gallery-{self.pk}"]
        if self.style:
            classes.append(f"gallery--{self.style}")
        return " ".join(classes)


class GalleryItem(CMSPlugin):
    image = models.ImageField(upload_to="ndthemes/gallery/")
    alt_text = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=255, blank=True, default="", help_text="Lightbox title.")

    def __str__(self):
        return self.title or self.alt_text or "Gallery image"


class ImageMultiple(CMSPlugin):
    LAYOUT_CHOICES = (
        ("tiled", "Tiled"),
        ("mosaic", "Mosaic"),
        ("mosaic-reversed", "Mosaic (reversed)"),
    )

    layout = models.CharField(max_length=16, choices=LAYOUT_CHOICES, default="tiled")

    def __str__(self):
        return f"Image multiple ({self.get_layout_display()})"

    def figure_class(self):
        return f"image image--{self.layout}"


class ImageMultipleItem(CMSPlugin):
    image = models.ImageField(upload_to="ndthemes/images/")
    alt_text = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.alt_text or "Image"


class ImageSingle(CMSPlugin):
    LAYOUT_CHOICES = (
        ("", "Default"),
        ("full-width", "Full width"),
        ("left", "Float left"),
        ("right", "Float right"),
        ("circle", "Circle"),
    )

    image = models.ImageField(upload_to="ndthemes/images/")
    alt_text = models.CharField(max_length=255, blank=True, default="")
    caption = models.CharField(max_length=4096, blank=True, default="")
    layout = models.CharField(max_length=16, choices=LAYOUT_CHOICES, blank=True, default="")

    def __str__(self):
        return self.caption or self.alt_text or "Image"

    def figure_class(self):
        classes = ["image"]
        if self.layout == "full-width":
            classes.append("image--full-width")
        elif self.layout == "left":
            classes.append("image-left")
        elif self.layout == "right":
            classes.append("image-right")
        elif self.layout == "circle":
            classes.append("image-circle")
        return " ".join(classes)


class Video(CMSPlugin):
    DISPLAY_CHOICES = (
        ("embed", "Embedded player"),
        ("placeholder", "Placeholder with play button"),
    )
    STYLE_CHOICES = (
        ("default", "Default"),
        ("minimal", "Minimal"),
        ("outline", "Outline"),
        ("ornamental", "Ornamental"),
    )
    ALIGNMENT_CHOICES = (
        ("", "Default"),
        ("left", "Float left"),
        ("right", "Float right"),
    )

    display_type = models.CharField(max_length=16, choices=DISPLAY_CHOICES, default="embed")
    video_url = models.URLField(help_text="YouTube or Vimeo URL.")
    label = models.CharField(max_length=255, blank=True, default="", help_text="Label for placeholder style.")
    style = models.CharField(max_length=16, choices=STYLE_CHOICES, default="default")
    alignment = models.CharField(max_length=16, choices=ALIGNMENT_CHOICES, blank=True, default="")

    def __str__(self):
        return self.label or self.video_url

    def embed_url(self):
        from .media_utils import video_embed_url

        return video_embed_url(self.video_url)

    def watch_url(self):
        from .media_utils import video_watch_url

        return video_watch_url(self.video_url)

    def thumbnail_url(self):
        from .media_utils import video_thumbnail_url

        return video_thumbnail_url(self.video_url)

    def file_type(self):
        from .media_utils import video_file_type

        return video_file_type(self.video_url)

    def wrapper_class(self):
        classes = ["video--wrapper"]
        if self.alignment:
            classes.append(f"video--{self.alignment}")
        return " ".join(classes)

    def placeholder_class(self):
        return f"video video--{self.style}"


class Avatar(CMSPlugin):
    SIZE_CHOICES = (
        ("xs", "Extra small"),
        ("sm", "Small"),
        ("md", "Medium"),
        ("lg", "Large"),
        ("xl", "Extra large"),
    )
    STYLE_CHOICES = (
        ("", "Default"),
        ("quote", "Quote"),
    )

    image = models.ImageField(upload_to="ndthemes/avatars/")
    alt_text = models.CharField(max_length=255, blank=True, default="")
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, default="md")
    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")
    caption = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.caption or self.alt_text or "Avatar"

    def avatar_class(self):
        classes = ["avatar", f"avatar--{self.size}"]
        if self.style:
            classes.append(f"avatar--{self.style}")
        return " ".join(classes)


class _LinkMixin(models.Model):
    link = PageField(blank=True, null=True)
    external_link = models.CharField(max_length=4096, blank=True, default="")

    class Meta:
        abstract = True

    def has_link(self):
        return bool(self.link_id or (self.external_link or "").strip())

    def get_href(self):
        if self.link_id:
            return self.link.get_absolute_url()
        href = (self.external_link or "").strip()
        return href or "#"

    def is_external(self):
        if self.link_id:
            return False
        href = (self.external_link or "").strip()
        return bool(href) and href not in {"#"}


class ButtonGroup(CMSPlugin):
    STYLE_CHOICES = (
        ("", "Default"),
        ("border", "With dividers"),
    )

    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")

    def __str__(self):
        return "Button group"

    def group_class(self):
        classes = ["no-bullets", "btn-group"]
        if self.style:
            classes.append(f"btn-group--{self.style}")
        return " ".join(classes)


class ButtonList(CMSPlugin):
    SIZE_CHOICES = (
        ("", "Default"),
        ("sm", "Small"),
        ("lg", "Large"),
    )

    size = models.CharField(max_length=8, choices=SIZE_CHOICES, blank=True, default="")

    def __str__(self):
        return "Button list"

    def list_class(self):
        classes = ["no-bullets", "btn-list"]
        if self.size:
            classes.append(f"btn-list--{self.size}")
        return " ".join(classes)


class ButtonItem(CMSPlugin, _LinkMixin):
    text = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class IconButton(CMSPlugin, _LinkMixin):
    ICON_CHOICES = (
        ("arrow-right", "Arrow right"),
        ("external-link", "External link"),
        ("download", "Download"),
        ("envelope", "Envelope"),
    )
    ALIGNMENT_CHOICES = (
        ("", "Left"),
        ("right", "Right"),
    )

    text = models.CharField(max_length=255)
    icon = models.CharField(max_length=32, choices=ICON_CHOICES, default="arrow-right")
    alignment = models.CharField(max_length=16, choices=ALIGNMENT_CHOICES, blank=True, default="")
    reveal_on_hover = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def button_class(self):
        classes = ["btn", "btn--icon"]
        if self.alignment:
            classes.append(f"btn--{self.alignment}")
        return " ".join(classes)


class LedeButton(CMSPlugin, _LinkMixin):
    text = models.CharField(max_length=512)

    def __str__(self):
        return self.text[:60]


class NavAnchor(CMSPlugin):
    label = models.CharField(max_length=255, blank=True, default="Anchor")

    def __str__(self):
        return self.label or "Navigation anchor"


class NavAnchorItem(CMSPlugin, _LinkMixin):
    text = models.CharField(max_length=255)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Pagination(CMSPlugin):
    def __str__(self):
        return "Pagination"


class PaginationItem(CMSPlugin, _LinkMixin):
    TYPE_CHOICES = (
        ("page", "Page"),
        ("current", "Current page"),
        ("disabled", "Disabled"),
        ("previous", "Previous"),
        ("next", "Next"),
    )

    label = models.CharField(max_length=32)
    item_type = models.CharField(max_length=16, choices=TYPE_CHOICES, default="page")

    def __str__(self):
        return self.label

    def item_class(self):
        if self.item_type == "current":
            return "current"
        if self.item_type == "disabled":
            return "disabled"
        if self.item_type == "previous":
            return "previous_page"
        if self.item_type == "next":
            return "next_page"
        return ""


class FootnoteList(CMSPlugin):
    def __str__(self):
        return "Footnotes"


class FootnoteItem(CMSPlugin):
    body = HTMLField()

    def __str__(self):
        return "Footnote"


class Dialog(CMSPlugin):
    STYLE_CHOICES = (
        ("", "Default"),
        ("narrow", "Narrow"),
        ("alert", "Alert"),
        ("notification", "Notification"),
        ("person", "With person"),
        ("video", "With video"),
    )

    trigger_text = models.CharField(max_length=255, default="Open dialog")
    heading = models.CharField(max_length=255)
    body = HTMLField()
    footer = models.TextField(blank=True, default="")
    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")

    def __str__(self):
        return self.heading

    def dialog_class(self):
        classes = ["dialog"]
        if self.style:
            classes.append(f"dialog--{self.style}")
        return " ".join(classes)


class FAQ(CMSPlugin):
    show_anchors = models.BooleanField(default=True)
    anchors_id = models.CharField(
        max_length=64,
        default="faq-list",
        help_text="ID for the anchor navigation list.",
    )
    show_back_to_top = models.BooleanField(default=True)

    def __str__(self):
        return "FAQ"


class FAQItem(CMSPlugin):
    question = models.CharField(max_length=512)
    item_id = models.CharField(
        max_length=64,
        help_text="Anchor ID for this item (e.g. faq_001).",
    )
    answer = HTMLField()

    def __str__(self):
        return self.question

    @property
    def search_fields(self):
        return ("question", "answer")


class Banner(CMSPlugin, _LinkMixin):
    LAYOUT_CHOICES = (
        ("stacked", "Stacked"),
        ("default", "Default (side by side)"),
        ("full", "Full width"),
        ("cards", "Cards"),
        ("accordion", "Accordion"),
        ("gallery", "Gallery"),
        ("mosaic", "Mosaic"),
        ("tiled", "Tiled"),
    )

    layout = models.CharField(max_length=16, choices=LAYOUT_CHOICES, default="stacked")
    title = models.CharField(max_length=255)
    caption = HTMLField(blank=True, default="")
    image = models.ImageField(upload_to="ndthemes/banners/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")
    link_text = models.CharField(max_length=255, blank=True, default="Learn more")
    intro_alignment = models.CharField(
        max_length=16,
        blank=True,
        default="",
        help_text='Optional intro alignment class (e.g. "text-center").',
    )

    def __str__(self):
        return self.title

    def section_intro_class(self):
        classes = ["section-intro"]
        if self.intro_alignment:
            classes.append(self.intro_alignment)
        return " ".join(classes)


class BannerImageItem(CMSPlugin):
    image = models.ImageField(upload_to="ndthemes/banners/")
    alt_text = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.alt_text or "Banner image"


class BannerAccordionItem(CMSPlugin):
    title = models.CharField(max_length=255)
    body = HTMLField()
    image = models.ImageField(upload_to="ndthemes/banners/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")
    open_by_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class PageHeader(CMSPlugin):
    VARIANT_CHOICES = (
        ("", "Default"),
        ("inset", "Inset"),
        ("container", "Container"),
        ("screen", "Screen"),
        ("fade", "Fade"),
        ("mosaic", "Mosaic"),
        ("tiled", "Tiled"),
    )
    TITLE_SIZE_CHOICES = (
        ("", "Default"),
        ("sm", "Small"),
        ("lg", "Large"),
        ("xl", "Extra large"),
    )

    title = models.CharField(max_length=512)
    lede = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="ndthemes/page-headers/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")
    title_size = models.CharField(max_length=8, choices=TITLE_SIZE_CHOICES, blank=True, default="")
    variant = models.CharField(max_length=16, choices=VARIANT_CHOICES, blank=True, default="")

    def __str__(self):
        return self.title

    def header_class(self):
        classes = ["page-header"]
        if self.variant:
            classes.append(f"page-header--{self.variant}")
        return " ".join(classes)

    def title_class(self):
        classes = ["page-title"]
        if self.title_size:
            classes.append(f"page-title--{self.title_size}")
        return " ".join(classes)


class _CardStyleMixin(models.Model):
    STYLE_CHOICES = (
        ("", "Default"),
        ("horizontal", "Horizontal"),
        ("compact", "Compact"),
        ("border", "Border"),
        ("image-sm", "Small image"),
        ("stacked", "Stacked"),
        ("image-right", "Image right"),
    )

    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")

    class Meta:
        abstract = True

    def card_modifier_class(self, base):
        classes = [base]
        if self.style:
            classes.append(f"{base}--{self.style}")
        return " ".join(classes)


class CardList(CMSPlugin):
    def __str__(self):
        return "Card list"


class CardGrid(CMSPlugin):
    def __str__(self):
        return "Card grid"


class CardDefault(CMSPlugin, _LinkMixin, _CardStyleMixin):
    title = models.CharField(max_length=512)
    summary = HTMLField(blank=True, default="")
    image = models.ImageField(upload_to="ndthemes/cards/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.title

    @property
    def search_fields(self):
        return ("title", "summary")

    def card_class(self):
        classes = ["card"]
        if self.style:
            classes.append(f"card--{self.style}")
        return " ".join(classes)


class CardNews(CMSPlugin, _LinkMixin, _CardStyleMixin):
    label = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=512)
    summary = HTMLField(blank=True, default="")
    image = models.ImageField(upload_to="ndthemes/cards/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")
    author_name = models.CharField(max_length=255, blank=True, default="")
    publish_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def search_fields(self):
        return ("label", "title", "summary", "author_name")

    def card_class(self):
        classes = ["card", "card--news"]
        if self.style:
            classes.append(f"card--{self.style}")
        return " ".join(classes)


class CardEvent(CMSPlugin, _LinkMixin):
    title = models.CharField(max_length=512)
    description = models.TextField(blank=True, default="")
    event_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=512, blank=True, default="")
    recurring = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def search_fields(self):
        return ("title", "description", "location")


class CardFeatured(CMSPlugin, _LinkMixin):
    label = models.CharField(max_length=255, blank=True, default="")
    title = models.CharField(max_length=512)
    image = models.ImageField(upload_to="ndthemes/cards/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.title

    @property
    def search_fields(self):
        return ("label", "title")


class CardPerson(CMSPlugin, _LinkMixin, _CardStyleMixin):
    title = models.CharField(max_length=512, help_text="Person name")
    job_title = HTMLField(blank=True, default="")
    summary = HTMLField(blank=True, default="")
    image = models.ImageField(upload_to="ndthemes/cards/", blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.title

    @property
    def search_fields(self):
        return ("title", "job_title", "summary")

    def card_class(self):
        classes = ["card", "card--person"]
        if self.style:
            classes.append(f"card--{self.style}")
        return " ".join(classes)


class CardBylineItem(CMSPlugin, _LinkMixin):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, default="", help_text="Role or affiliation")
    image = models.ImageField(upload_to="ndthemes/cards/", blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def search_fields(self):
        return ("name", "title")


class CardMediaMention(CMSPlugin, _LinkMixin):
    publication_name = models.CharField(max_length=255)
    publication_slug = models.CharField(
        max_length=64,
        blank=True,
        default="",
        help_text="Optional CSS class for publication styling (e.g. npr, nyt).",
    )
    publication_logo = models.ImageField(upload_to="ndthemes/publications/", blank=True, null=True)
    title = models.CharField(max_length=512)
    summary = HTMLField(blank=True, default="")
    mention_date = models.CharField(max_length=64, blank=True, default="")
    meta_heading = models.CharField(max_length=64, blank=True, default="Mentions")

    def __str__(self):
        return self.title

    @property
    def search_fields(self):
        return ("publication_name", "title", "summary")

    def card_class(self):
        classes = ["card", "card--media-mention"]
        if self.publication_slug:
            classes.append(self.publication_slug)
        return " ".join(classes)


class CardMediaMentionQuoted(CMSPlugin, _LinkMixin):
    publication_name = models.CharField(max_length=255)
    publication_slug = models.CharField(max_length=64, blank=True, default="")
    publication_logo = models.ImageField(upload_to="ndthemes/publications/", blank=True, null=True)
    quote = HTMLField()
    link_text = models.CharField(max_length=64, default="Read article")

    def __str__(self):
        return self.publication_name

    @property
    def search_fields(self):
        return ("publication_name", "quote")

    def card_class(self):
        classes = ["card", "card--media-mention-quoted"]
        if self.publication_slug:
            classes.append(self.publication_slug)
        return " ".join(classes)


class Button(CMSPlugin, _LinkMixin):
    STYLE_CHOICES = (
        ("", "Default"),
        ("cta", "Call to action"),
        ("secondary", "Secondary"),
        ("tertiary", "Tertiary"),
        ("neutral", "Neutral"),
        ("more", "More"),
    )

    text = models.CharField(max_length=255)
    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")

    def __str__(self):
        return self.text

    def button_class(self):
        classes = ["btn"]
        if self.style:
            classes.append(f"btn--{self.style}")
        return " ".join(classes)


class Byline(CMSPlugin, _LinkMixin):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, default="", help_text="Role or affiliation")
    image = models.ImageField(upload_to="ndthemes/bylines/", blank=True, null=True)

    def __str__(self):
        return self.name


class SocialShare(CMSPlugin):
    def __str__(self):
        return "Social share"


class VideoButton(CMSPlugin, _LinkMixin):
    STYLE_CHOICES = (
        ("", "Default"),
        ("minimal", "Minimal"),
        ("ornamental", "Ornamental"),
        ("outline", "Outline"),
    )

    text = models.CharField(max_length=255, default="View video")
    style = models.CharField(max_length=16, choices=STYLE_CHOICES, blank=True, default="")

    def __str__(self):
        return self.text

    def button_class(self):
        classes = ["btn", "btn--video"]
        if self.style:
            classes.append(f"video--{self.style}")
        return " ".join(classes)


class Icon(CMSPlugin):
    ICON_CHOICES = (
        ("search", "Search"),
        ("arrow-right", "Arrow right"),
        ("external-link", "External link"),
        ("download", "Download"),
        ("envelope", "Envelope"),
        ("clock", "Clock"),
        ("map-pin", "Map pin"),
        ("facebook", "Facebook"),
        ("linkedin", "LinkedIn"),
        ("twitter-x", "X/Twitter"),
        ("box-arrow-up", "Share"),
    )
    SIZE_CHOICES = (
        ("", "Default"),
        ("sm", "Small"),
        ("lg", "Large"),
        ("xl", "Extra large"),
    )

    icon = models.CharField(max_length=32, choices=ICON_CHOICES, default="arrow-right")
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, blank=True, default="")
    label = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.label or self.get_icon_display()

    def icon_class(self):
        classes = ["icon"]
        if self.size:
            classes.append(f"icon--{self.size}")
        return " ".join(classes)


class Sticker(CMSPlugin):
    SIZE_CHOICES = (
        ("", "Default"),
        ("sm", "Small"),
        ("lg", "Large"),
        ("xl", "Extra large"),
    )

    sticker = models.CharField(max_length=32, choices=STICKER_CHOICES, default="backpack")
    size = models.CharField(max_length=8, choices=SIZE_CHOICES, blank=True, default="")
    label = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.label or self.get_sticker_display()

    def sticker_class(self):
        classes = ["sticker"]
        if self.size:
            classes.append(f"sticker--{self.size}")
        return " ".join(classes)


class Form(CMSPlugin):
    title = models.CharField(max_length=255, blank=True, default="")
    submit_label = models.CharField(max_length=64, default="Submit")

    def __str__(self):
        return self.title or "Form"


class FormField(CMSPlugin):
    TYPE_CHOICES = (
        ("text", "Text"),
        ("email", "Email"),
        ("password", "Password"),
        ("number", "Number"),
        ("date", "Date"),
        ("search", "Search"),
        ("textarea", "Textarea"),
        ("select", "Select"),
        ("checkbox_list", "Checkbox list"),
        ("radio_list", "Radio list"),
        ("switch", "Switch"),
    )

    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=16, choices=TYPE_CHOICES, default="text")
    field_id = models.SlugField(max_length=64, help_text="Unique field id for labels/inputs.")
    input_placeholder = models.CharField(max_length=255, blank=True, default="")
    options = models.TextField(
        blank=True,
        default="",
        help_text="One option per line (for select, checkbox, radio).",
    )
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def option_list(self):
        return [line.strip() for line in self.options.splitlines() if line.strip()]


class SearchForm(CMSPlugin):
    label = models.CharField(max_length=255, default="Search", help_text="Accessible label for the search field.")
    input_placeholder = models.CharField(max_length=255, blank=True, default="Search…")
    action = models.CharField(max_length=512, blank=True, default="/search/")

    def __str__(self):
        return self.label
