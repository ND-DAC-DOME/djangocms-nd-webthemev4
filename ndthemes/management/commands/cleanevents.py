from django.core.management.base import BaseCommand

from ndthemes.models import Event, EventSeries, PagePreviewExtension, PageTag


class Command(BaseCommand):
    help = "Ensures every Event/EventSeries page carries the 'Event' PageTag."

    def handle(self, *args, **options):
        tag, _created = PageTag.objects.get_or_create(tag="Event")

        for event in Event.objects.all():
            extension = PagePreviewExtension.objects.filter(extended_object=event.page).first()
            if extension and tag not in extension.tags.all():
                extension.tags.add(tag)
                self.stdout.write(f"  ...added event tag to page {event.page}")

        for series in EventSeries.objects.all():
            extension = PagePreviewExtension.objects.filter(extended_object=series.page).first()
            if extension and tag not in extension.tags.all():
                extension.tags.add(tag)
                self.stdout.write(f"  ...added event tag to page {series.page}")

        self.stdout.write(self.style.SUCCESS("Successfully cleaned event pages."))
