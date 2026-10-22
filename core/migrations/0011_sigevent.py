# Generated manually for SIGEvent

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_internalconsultation_brief_document_meeting_agenda_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SIGEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("desc", models.TextField(blank=True)),
                ("event_datetime", models.DateTimeField()),
                (
                    "type",
                    models.CharField(
                        choices=[("workshop", "Workshop"), ("meeting", "Meeting"), ("conference", "Conference")],
                        max_length=50,
                    ),
                ),
                ("join", models.URLField(blank=True, null=True)),
                (
                    "sig_scope",
                    models.CharField(
                        choices=[
                            ("All", "All SIGs"),
                            ("FI", "Future of Internet"),
                            ("TPS", "Internet Protocols & Standards"),
                            ("DNN", "Domain Names & Related Issues"),
                            ("Joint", "SIG Joint"),
                        ],
                        default="All",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "SIG event",
                "verbose_name_plural": "SIG events",
                "ordering": ("event_datetime",),
            },
        ),
    ]
