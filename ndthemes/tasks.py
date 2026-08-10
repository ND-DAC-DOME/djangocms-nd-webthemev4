"""
Auto-archive Celery task, replacing v3's ``django_cog``-scheduled version.

This project uses plain Celery + django-celery-beat (see
``CELERY_BEAT_SCHEDULE`` in settings) rather than ``django_cog``.
"""
import datetime as DT

from celery import shared_task
from django.utils import timezone


@shared_task(name="ndthemes.auto_archive_events")
def auto_archive_events():
    from .models import ArchivePageExtension, DateTime, Setting
    from .utils import pages_with_template

    try:
        auto_archive = Setting.objects.get(key="Auto-archive events")
    except Setting.DoesNotExist:
        return

    if not auto_archive.enabled:
        return

    current_time_tz = timezone.now()

    for event_page in pages_with_template("event_detail.html"):
        datetime_obj = DateTime.objects.filter(placeholder__in=event_page.get_placeholders("en")).first()

        archive, _created = ArchivePageExtension.objects.get_or_create(extended_object=event_page)
        if archive.archive_now:
            continue

        if archive.schedule_archive:
            if current_time_tz >= archive.schedule_archive:
                archive.archive_now = True
                archive.save()
            continue

        if not datetime_obj or not datetime_obj.start_date:
            continue

        date_to_check = datetime_obj.end_date or datetime_obj.start_date
        threshold = DT.datetime.combine(date_to_check, datetime_obj.end_time or datetime_obj.start_time or DT.time.min)
        threshold = timezone.make_aware(threshold) if timezone.is_naive(threshold) else threshold

        if current_time_tz >= threshold:
            archive.archive_now = True
            archive.save()
