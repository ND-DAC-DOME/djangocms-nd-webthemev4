from django.contrib import admin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

from cms.extensions import PageExtensionAdmin

from .models import (
    ArchivePageExtension,
    Event,
    EventSeries,
    PageContentIndex,
    PagePreviewExtension,
    PageTag,
    RecurringEvent,
    Setting,
)


@admin.register(PageContentIndex)
class PageContentIndexAdmin(admin.ModelAdmin):
    list_display = ("page", "plugin_id")
    search_fields = ("content",)


@admin.register(PagePreviewExtension)
class PagePreviewExtensionAdmin(PageExtensionAdmin):
    pass


@admin.register(ArchivePageExtension)
class ArchivePageExtensionAdmin(PageExtensionAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("key", "setting")
    search_fields = ("key",)
    list_filter = ("setting_type",)
    ordering = ("key",)
    readonly_fields = ("key",)
    fieldsets = ((None, {"fields": ("setting_type", "value", "enabled", "page")}),)

    def setting(self, obj):
        if obj.setting_type == "text":
            return obj.value
        if obj.setting_type == "boolean":
            return obj.enabled
        if obj.setting_type == "page":
            return obj.page
        return None


@admin.register(PageTag)
class PageTagAdmin(admin.ModelAdmin):
    list_display = ("tag", "search_category", "archive_category")
    search_fields = ("tag",)
    list_filter = ("search_category", "archive_category")
    ordering = ("tag",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "start", "end", "location")
    search_fields = ("name", "location")
    list_filter = ("recurring_event", "series")
    ordering = ("name",)
    fieldsets = ((None, {"fields": ("series", "name", "start", "end", "location", "map_link")}),)
    actions = ["bulk_delete", "create_recurring_event"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def bulk_delete(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, "Events deleted!")

    bulk_delete.short_description = "Delete selected events"

    def create_recurring_event(self, request, queryset):
        new_event = None
        for obj in queryset:
            if not obj.recurring_event:
                recurring_event = RecurringEvent()
                recurring_event.save()
                obj.recurring_event = recurring_event
                obj.save()
            new_event = Event(
                name=obj.name,
                location=obj.location,
                map_link=obj.map_link,
                recurring_event=obj.recurring_event,
            )
            new_event.save()

        if queryset.count() == 1 and new_event:
            self.message_user(request, "New event created! Please fill out the date of your new event below.")
            return HttpResponseRedirect(reverse("admin:ndthemes_event_change", args=[new_event.pk]))

        self.message_user(request, f"{queryset.count()} new recurring events have been created.")
        return HttpResponseRedirect(reverse("admin:ndthemes_event_changelist"))

    create_recurring_event.short_description = "Create Recurring Events"


@admin.register(EventSeries)
class EventSeriesAdmin(admin.ModelAdmin):
    list_display = ("name", "event_count")
    search_fields = ("name",)
    ordering = ("name",)
    actions = ["bulk_delete"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def event_count(self, obj):
        return obj.events.count()

    def bulk_delete(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, "Event series deleted!")

    bulk_delete.short_description = "Delete selected event series"
