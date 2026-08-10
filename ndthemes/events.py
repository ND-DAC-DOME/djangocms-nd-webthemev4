from django.shortcuts import render

from cms.models import PageUrl

from .models import Event


def recurring_events(request, slug):
    """List every event sharing a ``RecurringEvent`` group, given any one event's slug."""
    page_url = PageUrl.objects.filter(slug=slug, language="en").first()
    if not page_url:
        return render(request, "404.html", {}, status=404)

    event = Event.objects.filter(page=page_url.page).first()
    if not event or not event.recurring_event:
        return render(request, "404.html", {}, status=404)

    events = Event.objects.filter(recurring_event=event.recurring_event).order_by("start")
    return render(
        request,
        "archive/event_group_listing.html",
        {"events": events, "title": event.name},
    )
