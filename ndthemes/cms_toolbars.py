from django.utils.translation import gettext_lazy as _

from cms.extensions.toolbar import ExtensionToolbar
from cms.toolbar_pool import toolbar_pool

from .models import ArchivePageExtension, PagePreviewExtension


@toolbar_pool.register
class PagePreviewExtensionToolbar(ExtensionToolbar):
    model = PagePreviewExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu:
            page_extension, url = self.get_page_extension_admin()
            if url:
                current_page_menu.add_modal_item(
                    _("Page Meta"), url=url, disabled=not self.toolbar.edit_mode_active, position=0
                )


@toolbar_pool.register
class ArchivePageExtensionToolbar(ExtensionToolbar):
    model = ArchivePageExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu:
            page_extension, url = self.get_page_extension_admin()
            if url:
                current_page_menu.add_modal_item(
                    _("Archive"), url=url, disabled=not self.toolbar.edit_mode_active, position=1
                )
