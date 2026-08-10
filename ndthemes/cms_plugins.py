"""
Plugin registrations for the ndthemes domain models.

Render templates here are intentionally minimal — M4 replaces them with
full NDT 4.0 Storybook markup. Registration, models, and admin options are
final as of M3.
"""
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    ArchiveLink,
    ButtonLink,
    ChildPageList,
    DateTime,
    EmailLink,
    EventList,
    EventsInsert,
    ExternalLink,
    FullWidthImage,
    Location,
    PageTagPlugin,
    PersonListGrid,
    PersonListItem,
    PersonListStacked,
    PhoneNumber,
    Ribbon,
    RibbonImage,
    RibbonImageAlt,
    SideNavigationChildList,
    SideNavigationDynamicFilter,
    SideNavigationPageLink,
    SimpleText,
    Triptych,
)


@plugin_pool.register_plugin
class TriptychPlugin(CMSPluginBase):
    model = Triptych
    name = _("Triptych (internal pages)")
    render_template = "plugins/triptych.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class DateTimePlugin(CMSPluginBase):
    model = DateTime
    name = _("Date and Time")
    render_template = "plugins/date_time.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class LocationPlugin(CMSPluginBase):
    model = Location
    name = _("Location")
    render_template = "plugins/location.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class ArchiveLinkPlugin(CMSPluginBase):
    model = ArchiveLink
    name = _("Archive Link")
    render_template = "plugins/archive_link.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class PhoneNumberPlugin(CMSPluginBase):
    model = PhoneNumber
    name = _("Phone Number")
    render_template = "plugins/phone_number.html"
    cache = False


@plugin_pool.register_plugin
class EventsPlugin(CMSPluginBase):
    model = EventsInsert
    name = _("Events Insert")
    render_template = "plugins/events_plugin.html"
    cache = False


@plugin_pool.register_plugin
class EventListPlugin(CMSPluginBase):
    model = EventList
    name = _("Event List")
    render_template = "plugins/events_list.html"
    cache = False


@plugin_pool.register_plugin
class PageTagPluginPlugin(CMSPluginBase):
    model = PageTagPlugin
    name = _("Page Tags")
    render_template = "plugins/page_tags.html"
    cache = False


@plugin_pool.register_plugin
class ButtonLinkPlugin(CMSPluginBase):
    model = ButtonLink
    name = _("Button Link")
    render_template = "plugins/button_link.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class EmailLinkPlugin(CMSPluginBase):
    model = EmailLink
    name = _("Email Link")
    render_template = "plugins/email_link.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class PersonGridListPlugin(CMSPluginBase):
    model = PersonListGrid
    name = _("Person List (Grid)")
    render_template = "plugins/people_list_grid.html"
    cache = False


@plugin_pool.register_plugin
class SimpleTextPlugin(CMSPluginBase):
    model = SimpleText
    name = _("Simple Text")
    render_template = "plugins/simple_text.html"
    cache = False


@plugin_pool.register_plugin
class PersonListStackedPlugin(CMSPluginBase):
    model = PersonListStacked
    name = _("Person List (Stacked)")
    render_template = "plugins/people_list_stacked.html"
    cache = False


@plugin_pool.register_plugin
class PersonListItemPlugin(CMSPluginBase):
    model = PersonListItem
    name = _("Person List Item")
    render_template = "plugins/person_list_item.html"
    cache = False


@plugin_pool.register_plugin
class SideNavigationChildListPlugin(CMSPluginBase):
    model = SideNavigationChildList
    name = _("Side Navigation Child Page List")
    render_template = "plugins/side_nav_children.html"
    cache = False


@plugin_pool.register_plugin
class SideNavigationPageLinkPlugin(CMSPluginBase):
    model = SideNavigationPageLink
    name = _("Side Navigation Page Link")
    render_template = "plugins/side_nav_pagelink.html"
    cache = False


@plugin_pool.register_plugin
class SideNavigationDynamicFilterPlugin(CMSPluginBase):
    model = SideNavigationDynamicFilter
    name = _("Side Navigation Dynamic Filter")
    render_template = "plugins/side_nav_dynamic_filter.html"
    cache = False


@plugin_pool.register_plugin
class RibbonPlugin(CMSPluginBase):
    model = Ribbon
    name = _("Ribbon")
    render_template = "plugins/ribbon.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class RibbonImagePlugin(CMSPluginBase):
    model = RibbonImage
    name = _("Ribbon with Image")
    render_template = "plugins/ribbon_with_image.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class RibbonImageAltPlugin(CMSPluginBase):
    model = RibbonImageAlt
    name = _("Ribbon with Image (alt)")
    render_template = "plugins/ribbon_with_image_alt.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class ChildPageListPlugin(CMSPluginBase):
    model = ChildPageList
    name = _("Generic Child Page List")
    render_template = "plugins/child_list.html"
    cache = False


@plugin_pool.register_plugin
class ExternalLinkPlugin(CMSPluginBase):
    model = ExternalLink
    name = _("External Link")
    render_template = "plugins/external_link.html"
    cache = False
    text_enabled = True


@plugin_pool.register_plugin
class FullWidthImagePlugin(CMSPluginBase):
    model = FullWidthImage
    name = _("Image (full width)")
    render_template = "plugins/full_width_image.html"
    cache = False
    text_enabled = True
