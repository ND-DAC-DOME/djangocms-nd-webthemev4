from django.db import migrations, models


def enable_root_second_level(apps, schema_editor):
    RootList = apps.get_model("ndthemes", "SideNavigationRootList")
    RootList.objects.filter(show_second_level_children=False).update(show_second_level_children=True)


class Migration(migrations.Migration):

    dependencies = [
        ("ndthemes", "0013_alter_sidenavigationchildlist_show_second_level_children_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sidenavigationrootlist",
            name="show_second_level_children",
            field=models.BooleanField(
                default=True,
                help_text="When enabled, nested links appear only under the current section branch.",
            ),
        ),
        migrations.RunPython(enable_root_second_level, migrations.RunPython.noop),
    ]
