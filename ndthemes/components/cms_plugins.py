from django.utils.translation import gettext_lazy as _

from cms.plugin_pool import plugin_pool

from .base import NDTPluginBase
from .models import (
    Accordion,
    AccordionItem,
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
    Heading,
    Icon,
    IconButton,
    ImageMultiple,
    ImageMultipleItem,
    ImageSingle,
    LedeButton,
    List,
    ListItem,
    NavAnchor,
    NavAnchorItem,
    Notice,
    PageHeader,
    Pagination,
    PaginationItem,
    Quote,
    SearchForm,
    SocialShare,
    Stat,
    StatList,
    Sticker,
    TabPanel,
    Table,
    Tabs,
    Timeline,
    TimelineItem,
    Video,
    VideoButton,
)


CARD_CHILD_PLUGINS = [
    "NDTCardDefaultPlugin",
    "NDTCardNewsPlugin",
    "NDTCardEventPlugin",
    "NDTCardFeaturedPlugin",
    "NDTCardPersonPlugin",
    "NDTCardMediaMentionPlugin",
    "NDTCardMediaMentionQuotedPlugin",
]

BANNER_CHILD_PLUGINS = CARD_CHILD_PLUGINS + [
    "NDTBannerImageItemPlugin",
    "NDTBannerAccordionItemPlugin",
    "NDTGalleryPlugin",
]


class NDTFormPluginBase(NDTPluginBase):
    module = _("NDT / Forms")


class NDTLayoutPluginBase(NDTPluginBase):
    module = _("NDT / Layout")


class NDTMediaPluginBase(NDTPluginBase):
    module = _("NDT / Media")


class NDTCardPluginBase(NDTPluginBase):
    module = _("NDT / Cards")


@plugin_pool.register_plugin
class NDTAccordionPlugin(NDTPluginBase):
    model = Accordion
    name = _("Accordion")
    render_template = "components/accordion.html"
    allow_children = True
    child_classes = ["NDTAccordionItemPlugin"]


@plugin_pool.register_plugin
class NDTAccordionItemPlugin(NDTPluginBase):
    model = AccordionItem
    name = _("Accordion item")
    render_template = "components/accordion_item.html"
    require_parent = True
    parent_classes = ["NDTAccordionPlugin"]
    allow_children = True


@plugin_pool.register_plugin
class NDTNoticePlugin(NDTPluginBase):
    model = Notice
    name = _("Notice")
    render_template = "components/notice.html"
    text_enabled = True


@plugin_pool.register_plugin
class NDTHeadingPlugin(NDTPluginBase):
    model = Heading
    name = _("Heading")
    render_template = "components/heading.html"
    text_enabled = True


@plugin_pool.register_plugin
class NDTQuotePlugin(NDTPluginBase):
    model = Quote
    name = _("Quote")
    render_template = "components/quote.html"
    text_enabled = True


@plugin_pool.register_plugin
class NDTStatListPlugin(NDTPluginBase):
    model = StatList
    name = _("Stat list")
    render_template = "components/stat_list.html"
    allow_children = True
    child_classes = ["NDTStatPlugin"]


@plugin_pool.register_plugin
class NDTStatPlugin(NDTPluginBase):
    model = Stat
    name = _("Stat")
    render_template = "components/stat.html"
    require_parent = True
    parent_classes = ["NDTStatListPlugin"]
    text_enabled = True


@plugin_pool.register_plugin
class NDTTabsPlugin(NDTLayoutPluginBase):
    model = Tabs
    name = _("Tabs")
    render_template = "components/tabs.html"
    allow_children = True
    child_classes = ["NDTTabPanelPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        children = list(getattr(instance, "child_plugin_instances", []) or [])
        active_pk = next((child.pk for child in children if child.active_by_default), None)
        if active_pk is None and children:
            active_pk = children[0].pk
        context["active_tab_pk"] = active_pk
        return context


@plugin_pool.register_plugin
class NDTTabPanelPlugin(NDTLayoutPluginBase):
    model = TabPanel
    name = _("Tab panel")
    render_template = "components/tab_panel.html"
    require_parent = True
    parent_classes = ["NDTTabsPlugin"]
    allow_children = True


@plugin_pool.register_plugin
class NDTListPlugin(NDTPluginBase):
    model = List
    name = _("List")
    render_template = "components/list.html"
    allow_children = True
    child_classes = ["NDTListItemPlugin"]


@plugin_pool.register_plugin
class NDTListItemPlugin(NDTPluginBase):
    model = ListItem
    name = _("List item")
    render_template = "components/list_item.html"
    require_parent = True
    parent_classes = ["NDTListPlugin"]
    text_enabled = True


@plugin_pool.register_plugin
class NDTTablePlugin(NDTPluginBase):
    model = Table
    name = _("Table")
    render_template = "components/table.html"
    text_enabled = True


@plugin_pool.register_plugin
class NDTTimelinePlugin(NDTPluginBase):
    model = Timeline
    name = _("Timeline")
    render_template = "components/timeline.html"
    allow_children = True
    child_classes = ["NDTTimelineItemPlugin"]


@plugin_pool.register_plugin
class NDTTimelineItemPlugin(NDTPluginBase):
    model = TimelineItem
    name = _("Timeline item")
    render_template = "components/timeline_item.html"
    require_parent = True
    parent_classes = ["NDTTimelinePlugin"]
    text_enabled = True


@plugin_pool.register_plugin
class NDTGalleryPlugin(NDTMediaPluginBase):
    model = Gallery
    name = _("Gallery")
    render_template = "components/gallery.html"
    allow_children = True
    child_classes = ["NDTGalleryItemPlugin"]


@plugin_pool.register_plugin
class NDTGalleryItemPlugin(NDTMediaPluginBase):
    model = GalleryItem
    name = _("Gallery image")
    render_template = "components/gallery_item.html"
    require_parent = True
    parent_classes = ["NDTGalleryPlugin"]


@plugin_pool.register_plugin
class NDTImageMultiplePlugin(NDTMediaPluginBase):
    model = ImageMultiple
    name = _("Image (multiple)")
    render_template = "components/image_multiple.html"
    allow_children = True
    child_classes = ["NDTImageMultipleItemPlugin"]


@plugin_pool.register_plugin
class NDTImageMultipleItemPlugin(NDTMediaPluginBase):
    model = ImageMultipleItem
    name = _("Image (multiple item)")
    render_template = "components/image_multiple_item.html"
    require_parent = True
    parent_classes = ["NDTImageMultiplePlugin"]


@plugin_pool.register_plugin
class NDTImageSinglePlugin(NDTMediaPluginBase):
    model = ImageSingle
    name = _("Image (single)")
    render_template = "components/image_single.html"


@plugin_pool.register_plugin
class NDTVideoPlugin(NDTMediaPluginBase):
    model = Video
    name = _("Video")
    render_template = "components/video.html"
    text_enabled = True


@plugin_pool.register_plugin
class NDTAvatarPlugin(NDTMediaPluginBase):
    model = Avatar
    name = _("Avatar")
    render_template = "components/avatar.html"


@plugin_pool.register_plugin
class NDTButtonGroupPlugin(NDTPluginBase):
    model = ButtonGroup
    name = _("Button group")
    render_template = "components/button_group.html"
    allow_children = True
    child_classes = ["NDTButtonItemPlugin"]


@plugin_pool.register_plugin
class NDTButtonListPlugin(NDTPluginBase):
    model = ButtonList
    name = _("Button list")
    render_template = "components/button_list.html"
    allow_children = True
    child_classes = ["NDTButtonItemPlugin"]


@plugin_pool.register_plugin
class NDTButtonItemPlugin(NDTPluginBase):
    model = ButtonItem
    name = _("Button")
    render_template = "components/button_item.html"
    require_parent = True
    parent_classes = ["NDTButtonGroupPlugin", "NDTButtonListPlugin"]


@plugin_pool.register_plugin
class NDTIconButtonPlugin(NDTPluginBase):
    model = IconButton
    name = _("Icon button")
    render_template = "components/icon_button.html"


@plugin_pool.register_plugin
class NDTLedeButtonPlugin(NDTPluginBase):
    model = LedeButton
    name = _("Lede button")
    render_template = "components/lede_button.html"


@plugin_pool.register_plugin
class NDTNavAnchorPlugin(NDTLayoutPluginBase):
    model = NavAnchor
    name = _("Navigation (anchor)")
    render_template = "components/nav_anchor.html"
    allow_children = True
    child_classes = ["NDTNavAnchorItemPlugin"]


@plugin_pool.register_plugin
class NDTNavAnchorItemPlugin(NDTLayoutPluginBase):
    model = NavAnchorItem
    name = _("Anchor link")
    render_template = "components/nav_anchor_item.html"
    require_parent = True
    parent_classes = ["NDTNavAnchorPlugin"]


@plugin_pool.register_plugin
class NDTPaginationPlugin(NDTPluginBase):
    model = Pagination
    name = _("Pagination")
    render_template = "components/pagination.html"
    allow_children = True
    child_classes = ["NDTPaginationItemPlugin"]


@plugin_pool.register_plugin
class NDTPaginationItemPlugin(NDTPluginBase):
    model = PaginationItem
    name = _("Pagination item")
    render_template = "components/pagination_item.html"
    require_parent = True
    parent_classes = ["NDTPaginationPlugin"]


@plugin_pool.register_plugin
class NDTFootnoteListPlugin(NDTPluginBase):
    model = FootnoteList
    name = _("Footnotes")
    render_template = "components/footnote_list.html"
    allow_children = True
    child_classes = ["NDTFootnoteItemPlugin"]
    text_enabled = True


@plugin_pool.register_plugin
class NDTFootnoteItemPlugin(NDTPluginBase):
    model = FootnoteItem
    name = _("Footnote")
    render_template = "components/footnote_item.html"
    require_parent = True
    parent_classes = ["NDTFootnoteListPlugin"]
    text_enabled = True


@plugin_pool.register_plugin
class NDTDialogPlugin(NDTPluginBase):
    model = Dialog
    name = _("Dialog")
    render_template = "components/dialog.html"
    text_enabled = True


@plugin_pool.register_plugin
class NDTFAQPlugin(NDTPluginBase):
    model = FAQ
    name = _("FAQ")
    render_template = "components/faq.html"
    allow_children = True
    child_classes = ["NDTFAQItemPlugin"]


@plugin_pool.register_plugin
class NDTFAQItemPlugin(NDTPluginBase):
    model = FAQItem
    name = _("FAQ item")
    render_template = "components/faq_item.html"
    require_parent = True
    parent_classes = ["NDTFAQPlugin"]
    text_enabled = True


@plugin_pool.register_plugin
class NDTBannerPlugin(NDTLayoutPluginBase):
    model = Banner
    name = _("Banner")
    render_template = "components/banner.html"
    allow_children = True
    child_classes = BANNER_CHILD_PLUGINS


@plugin_pool.register_plugin
class NDTBannerImageItemPlugin(NDTLayoutPluginBase):
    model = BannerImageItem
    name = _("Banner image")
    render_template = "components/banner_image_item.html"
    require_parent = True
    parent_classes = ["NDTBannerPlugin"]


@plugin_pool.register_plugin
class NDTBannerAccordionItemPlugin(NDTLayoutPluginBase):
    model = BannerAccordionItem
    name = _("Banner accordion panel")
    render_template = "components/banner_accordion_item.html"
    require_parent = True
    parent_classes = ["NDTBannerPlugin"]
    text_enabled = True


@plugin_pool.register_plugin
class NDTPageHeaderPlugin(NDTLayoutPluginBase):
    model = PageHeader
    name = _("Page header")
    render_template = "components/page_header.html"


@plugin_pool.register_plugin
class NDTCardListPlugin(NDTCardPluginBase):
    model = CardList
    name = _("Card list")
    render_template = "components/card_list.html"
    allow_children = True
    child_classes = CARD_CHILD_PLUGINS


@plugin_pool.register_plugin
class NDTCardDefaultPlugin(NDTCardPluginBase):
    model = CardDefault
    name = _("Card (default)")
    render_template = "components/card_default.html"


@plugin_pool.register_plugin
class NDTCardNewsPlugin(NDTCardPluginBase):
    model = CardNews
    name = _("Card (news)")
    render_template = "components/card_news.html"


@plugin_pool.register_plugin
class NDTCardEventPlugin(NDTCardPluginBase):
    model = CardEvent
    name = _("Card (event)")
    render_template = "components/card_event.html"


@plugin_pool.register_plugin
class NDTCardFeaturedPlugin(NDTCardPluginBase):
    model = CardFeatured
    name = _("Card (featured)")
    render_template = "components/card_featured.html"


@plugin_pool.register_plugin
class NDTCardPersonPlugin(NDTCardPluginBase):
    model = CardPerson
    name = _("Card (people)")
    render_template = "components/card_person.html"


@plugin_pool.register_plugin
class NDTCardBylineItemPlugin(NDTCardPluginBase):
    model = CardBylineItem
    name = _("Card byline")
    render_template = "components/card_byline_item.html"
    require_parent = True
    parent_classes = ["NDTCardMediaMentionPlugin", "NDTCardMediaMentionQuotedPlugin"]


@plugin_pool.register_plugin
class NDTCardMediaMentionPlugin(NDTCardPluginBase):
    model = CardMediaMention
    name = _("Card (media mention)")
    render_template = "components/card_media_mention.html"
    allow_children = True
    child_classes = ["NDTCardBylineItemPlugin"]


@plugin_pool.register_plugin
class NDTCardMediaMentionQuotedPlugin(NDTCardPluginBase):
    model = CardMediaMentionQuoted
    name = _("Card (media mention, quoted)")
    render_template = "components/card_media_mention_quoted.html"
    allow_children = True
    child_classes = ["NDTCardBylineItemPlugin"]


@plugin_pool.register_plugin
class NDTButtonPlugin(NDTPluginBase):
    model = Button
    name = _("Button")
    render_template = "components/button.html"


@plugin_pool.register_plugin
class NDTBylinePlugin(NDTPluginBase):
    model = Byline
    name = _("Byline")
    render_template = "components/byline.html"


@plugin_pool.register_plugin
class NDTSocialSharePlugin(NDTPluginBase):
    model = SocialShare
    name = _("Social share")
    render_template = "components/social_share.html"


@plugin_pool.register_plugin
class NDTVideoButtonPlugin(NDTPluginBase):
    model = VideoButton
    name = _("Video button")
    render_template = "components/video_button.html"


@plugin_pool.register_plugin
class NDTIconPlugin(NDTPluginBase):
    model = Icon
    name = _("Icon")
    render_template = "components/icon.html"


@plugin_pool.register_plugin
class NDTStickerPlugin(NDTPluginBase):
    model = Sticker
    name = _("Sticker")
    render_template = "components/sticker.html"


@plugin_pool.register_plugin
class NDTFormPlugin(NDTFormPluginBase):
    model = Form
    name = _("Form")
    render_template = "components/form.html"
    allow_children = True
    child_classes = ["NDTFormFieldPlugin"]


@plugin_pool.register_plugin
class NDTFormFieldPlugin(NDTFormPluginBase):
    model = FormField
    name = _("Form field")
    render_template = "components/form_field.html"
    require_parent = True
    parent_classes = ["NDTFormPlugin"]


@plugin_pool.register_plugin
class NDTSearchFormPlugin(NDTFormPluginBase):
    model = SearchForm
    name = _("Search form")
    render_template = "components/search_form.html"
