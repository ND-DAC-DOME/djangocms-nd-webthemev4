from cms.plugin_base import CMSPluginBase
from django.utils.translation import gettext_lazy as _


class NDTPluginBase(CMSPluginBase):
    """Shared defaults for NDT4 component plugins."""

    cache = False
    module = _("NDT / Content")
