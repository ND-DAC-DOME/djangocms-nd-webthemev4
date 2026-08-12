from django.core.management.base import BaseCommand

from cms.models import Page

from ndthemes.signals import reindex_page


class Command(BaseCommand):
    help = (
        "Rebuild PageContentIndex for all CMS pages so plugin content "
        "(people cards, text, FAQs, etc.) is searchable."
    )

    def handle(self, *args, **options):
        pages = Page.objects.all()
        total = pages.count()
        indexed = 0

        for page in pages.iterator():
            reindex_page(page)
            indexed += 1
            if indexed % 25 == 0 or indexed == total:
                self.stdout.write(f"  ...indexed {indexed}/{total} pages")

        self.stdout.write(self.style.SUCCESS(f"Reindexed search content for {indexed} pages."))
