# Generated manually for Research module

import django.db.models.deletion
from django.db import migrations, models


def seed_broad_topics(apps, schema_editor):
    ResearchBroadTopic = apps.get_model("core", "ResearchBroadTopic")
    defaults = [
        ("Domain Names", "domain-names", 10),
        ("Internet Protocols", "internet-protocols", 20),
        ("Standards", "standards", 30),
        ("AI and Emerging Tech", "ai-and-emerging-tech", 40),
        ("NIXI and India-specific", "nixi-and-india-specific", 50),
    ]
    for name, slug, order in defaults:
        ResearchBroadTopic.objects.get_or_create(
            slug=slug,
            defaults={"name": name, "sort_order": order, "is_active": True},
        )


def unseed_broad_topics(apps, schema_editor):
    ResearchBroadTopic = apps.get_model("core", "ResearchBroadTopic")
    ResearchBroadTopic.objects.filter(
        slug__in=[
            "domain-names",
            "internet-protocols",
            "standards",
            "ai-and-emerging-tech",
            "nixi-and-india-specific",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_alter_sigmember_user_delete_customuser"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResearchBroadTopic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=220, unique=True)),
                ("description", models.TextField(blank=True)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Research broad topic",
                "verbose_name_plural": "Research broad topics",
                "ordering": ("sort_order", "name"),
            },
        ),
        migrations.CreateModel(
            name="OpenSourceProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255)),
                ("description", models.TextField()),
                ("status", models.CharField(choices=[("pending", "Pending approval"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("proposed_by_email", models.EmailField(blank=True, max_length=254)),
                ("proposed_by_name", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("broad_topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="open_source_projects", to="core.researchbroadtopic")),
            ],
            options={
                "verbose_name": "Open source project",
                "verbose_name_plural": "Open source projects",
                "ordering": ("broad_topic", "name"),
                "unique_together": {("broad_topic", "slug")},
            },
        ),
        migrations.CreateModel(
            name="ResearchSpecificTopic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255)),
                ("status", models.CharField(choices=[("pending", "Pending approval"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("proposed_by_email", models.EmailField(blank=True, max_length=254)),
                ("proposed_by_name", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("broad_topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="specific_research_topics", to="core.researchbroadtopic")),
            ],
            options={
                "verbose_name": "Research specific topic",
                "verbose_name_plural": "Research specific topics",
                "ordering": ("broad_topic", "name"),
                "unique_together": {("broad_topic", "slug")},
            },
        ),
        migrations.CreateModel(
            name="ResearchPaper",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("version", models.PositiveIntegerField(editable=False, help_text="Auto-assigned: next integer for this specific topic.")),
                ("title", models.CharField(max_length=500)),
                ("abstract", models.TextField(help_text="Short abstract (about 2–3 sentences).")),
                ("document", models.FileField(help_text="PDF or Word document.", upload_to="research/papers/%Y/%m/")),
                ("is_nixi_intern", models.BooleanField(default=False)),
                ("internship_batch_or_year", models.CharField(blank=True, max_length=120)),
                ("submitter_display_name", models.CharField(max_length=200)),
                ("submitter_email", models.EmailField(max_length=254)),
                ("submitter_account_id", models.IntegerField(blank=True, help_text="ig_account.id when submitted via portal login.", null=True)),
                ("status", models.CharField(choices=[("pending", "Pending approval"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("specific_topic", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="papers", to="core.researchspecifictopic")),
            ],
            options={
                "verbose_name": "Research paper",
                "verbose_name_plural": "Research papers",
                "ordering": ("-version", "-uploaded_at"),
            },
        ),
        migrations.CreateModel(
            name="OpenSourceContribution",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("version", models.PositiveIntegerField(editable=False, help_text="Auto-assigned per project.")),
                ("title", models.CharField(help_text="Short title for this contribution.", max_length=300)),
                ("summary", models.TextField(blank=True)),
                ("contribution_file", models.FileField(blank=True, help_text="Optional file (PDF, Word, etc.).", null=True, upload_to="research/oss/%Y/%m/")),
                ("external_url", models.URLField(blank=True, max_length=500)),
                ("contributor_display_name", models.CharField(max_length=200)),
                ("contributor_email", models.EmailField(max_length=254)),
                ("contributor_account_id", models.IntegerField(blank=True, null=True)),
                ("status", models.CharField(choices=[("pending", "Pending approval"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="contributions", to="core.opensourceproject")),
            ],
            options={
                "verbose_name": "Open source contribution",
                "verbose_name_plural": "Open source contributions",
                "ordering": ("-version", "-uploaded_at"),
            },
        ),
        migrations.RunPython(seed_broad_topics, unseed_broad_topics),
    ]
