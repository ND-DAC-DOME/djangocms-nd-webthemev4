# Generated manually for SideNavigationRootList

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cms", "0043_alter_globalpagepermission_can_view_and_more"),
        ("ndthemes", "0011_cardgrid_person_job_title_html"),
    ]

    operations = [
        migrations.CreateModel(
            name="SideNavigationRootList",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="%(app_label)s_%(class)s",
                        serialize=False,
                        to="cms.cmsplugin",
                    ),
                ),
                (
                    "link_order",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("page-tree", "Page Order"),
                            ("name-asc", "Title (A → Z)"),
                            ("name-desc", "Title (Z → A)"),
                            ("date-asc", "Publication Date (Newest → Oldest)"),
                            ("date-desc", "Publication Date (Oldest → Newest)"),
                        ],
                        default="page-tree",
                        max_length=255,
                        null=True,
                    ),
                ),
                ("show_second_level_children", models.BooleanField(default=False)),
                (
                    "child_link_order",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("page-tree", "Page Order"),
                            ("name-asc", "Title (A → Z)"),
                            ("name-desc", "Title (Z → A)"),
                            ("date-asc", "Publication Date (Newest → Oldest)"),
                            ("date-desc", "Publication Date (Oldest → Newest)"),
                        ],
                        default="page-tree",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="side_navigation_root_list_filters",
                        to="ndthemes.pagetag",
                    ),
                ),
            ],
            bases=("cms.cmsplugin",),
        ),
    ]
