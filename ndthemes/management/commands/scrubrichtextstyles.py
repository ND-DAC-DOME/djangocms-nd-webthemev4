from django.apps import apps
from django.core.management.base import BaseCommand

from djangocms_text.fields import HTMLField
from djangocms_text.models import Text

from ndthemes.richtext import scrub_document, scrub_inline_styles


class Command(BaseCommand):
    help = (
        "Removes hard-coded colours and fonts from stored rich text so body copy "
        "follows the NDT theme tokens. New content is scrubbed on save; this fixes "
        "content that was pasted in before that."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would change without writing to the database.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        changed = self.scrub_text_plugins(dry_run) + self.scrub_html_fields(dry_run)

        if dry_run:
            self.stdout.write(self.style.WARNING(f"Dry run: {changed} record(s) would be updated."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Scrubbed inline styles from {changed} record(s)."))

    def scrub_text_plugins(self, dry_run):
        changed = 0
        for plugin in Text.objects.all().iterator():
            body = scrub_inline_styles(plugin.body)
            json = scrub_document(plugin.json) if plugin.json else plugin.json
            if body == plugin.body and json == plugin.json:
                continue
            changed += 1
            self.stdout.write(f"  ...Text plugin {plugin.pk} ({plugin})")
            if not dry_run:
                # Bypass Text.save(), which re-runs sanitising and hyphenation.
                Text.objects.filter(pk=plugin.pk).update(body=body, json=json)
        return changed

    def scrub_html_fields(self, dry_run):
        changed = 0
        for model in apps.get_models():
            names = [field.name for field in model._meta.concrete_fields if isinstance(field, HTMLField)]
            if not names:
                continue
            for instance in model.objects.all().iterator():
                updates = {}
                for name in names:
                    value = getattr(instance, name, None)
                    if value:
                        scrubbed = scrub_inline_styles(value)
                        if scrubbed != value:
                            updates[name] = scrubbed
                if not updates:
                    continue
                changed += 1
                self.stdout.write(f"  ...{model._meta.label} {instance.pk} ({', '.join(updates)})")
                if not dry_run:
                    model.objects.filter(pk=instance.pk).update(**updates)
        return changed
