from django.db import migrations, models
import django.db.models.deletion


FORUMS = [
    {
        "slug": "icann",
        "name": "ICANN",
        "tagline": "Internet identifiers, DNS and naming policy",
        "logo_style": "wide",
        "logo_url": "https://itp.cdn.icann.org/assets/images/www-static/logo/icann-logo-tagline-en_680x152.webp",
        "sort_order": 1,
        "positions": [
            ("2025-03-01", "ccNSO guidance on DNS abuse metrics", "India noted the need for metrics that respect national legal frameworks and encouraged transparent reporting without duplicating local enforcement.", "ccNSO session"),
            ("2025-01-22", "New gTLD subsequent rounds — public comment", "Submission emphasised affordability for applicants from developing economies and clarity on geographic and cultural string protections.", "Public comment summary"),
            ("2024-11-08", "GNSO policy development on privacy proxy services", "Aligned with MeitY-led stakeholder consultations on balancing WHOIS utility with data protection under Indian law.", "GNSO materials"),
        ],
    },
    {
        "slug": "igf",
        "name": "Internet Governance Forum (IGF)",
        "tagline": "Multi-stakeholder dialogue on global Internet policy",
        "logo_style": "tall",
        "logo_url": "https://www.intgovforum.org/sites/default/files/igflogo2.png",
        "sort_order": 2,
        "positions": [
            ("2025-02-18", "IGF 2025 thematic inputs — AI and connectivity", "India highlighted inclusive AI governance, open standards, and last-mile connectivity investments as national priorities.", "National IGF track"),
            ("2024-12-05", "WSIS+20 review — development dimension", "Stressed bridging digital divides, capacity building, and meaningful participation for Global South delegations.", "WSIS coordination"),
            ("2024-09-14", "Cybersecurity and trust — main session intervention", "Called for norms that strengthen resilience while respecting sovereignty and cross-border cooperation on incident response.", "IGF session record"),
        ],
    },
    {
        "slug": "apnic",
        "name": "APNIC",
        "tagline": "Asia–Pacific Internet number resources",
        "logo_style": "standard",
        "logo_url": "https://webdist.data.apnic.net/web-framework-theme/9.1.5/images/apnic.svg",
        "sort_order": 3,
        "positions": [
            ("2025-01-30", "IPv6 deployment and measurement", "Supported APNIC community efforts on accurate routing data and IPv6 adoption reporting for the region, including Indian ISPs.", "APNIC conference workshop"),
            ("2024-10-21", "RPKI and routing security", "India reiterated commitment to ROA uptake and collaboration on anti-hijack practices with neighbouring economies.", "Routing SIG"),
        ],
    },
    {
        "slug": "itu",
        "name": "ITU",
        "tagline": "Telecommunication standardisation and development",
        "logo_style": "standard",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/International_Telecommunication_Union_logo.svg/480px-International_Telecommunication_Union_logo.svg.png",
        "sort_order": 4,
        "positions": [
            ("2025-02-27", "WTSA and standardisation priorities", "Underlined interoperability, security-by-design, and reference to existing multistakeholder Internet governance processes.", "Delegation brief"),
            ("2024-08-19", "Development — digital public infrastructure", "Shared India Stack–inspired lessons on identity, payments, and consent-based data sharing for sustainable development goals.", "ITU-D forum"),
        ],
    },
    {
        "slug": "w3c",
        "name": "W3C",
        "tagline": "Web standards and accessibility",
        "logo_style": "standard",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/W3C_icon.svg/480px-W3C_icon.svg.png",
        "sort_order": 5,
        "positions": [
            ("2025-03-12", "Web accessibility and Indian languages", "Encouraged WCAG adoption in e-governance templates and Indic script shaping improvements in browser engines.", "WAI community"),
            ("2024-12-01", "Privacy-preserving web APIs", "Contributed to discussion on advertising technology changes while preserving user agency and regulatory alignment.", "WebPM WG note"),
        ],
    },
]

HIGHLIGHTS = [
    ("https://images.unsplash.com/photo-1526304760382-3591ee3c7604?auto=format&fit=crop&w=1600&q=80", "Delegates in a conference hall", "India’s engagement in multistakeholder Internet governance dialogues.", 1),
    ("https://images.unsplash.com/photo-1540575467063-27aef4e929bd?auto=format&fit=crop&w=1600&q=80", "Panel discussion at a summit", "National and regional forums feeding into global policy tracks.", 2),
    ("https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=1600&q=80", "Audience at a technology event", "Stakeholder consultations supporting India’s international positions.", 3),
    ("https://images.unsplash.com/photo-1504384308090-c54be3855833?auto=format&fit=crop&w=1600&q=80", "Workspace with a connectivity theme", "Capacity building and research inputs for global standards bodies.", 4),
]


def seed_global_forums(apps, schema_editor):
    Page = apps.get_model("core", "GlobalForumPage")
    Forum = apps.get_model("core", "GlobalForum")
    Position = apps.get_model("core", "GlobalForumPosition")
    Highlight = apps.get_model("core", "GlobalForumHighlight")
    if not Page.objects.exists():
        Page.objects.create()
    if Forum.objects.exists():
        return
    for item in FORUMS:
        forum = Forum.objects.create(
            slug=item["slug"],
            name=item["name"],
            tagline=item["tagline"],
            logo_style=item["logo_style"],
            logo_url=item["logo_url"],
            sort_order=item["sort_order"],
            is_published=True,
        )
        for statement_date, title, summary, source in item["positions"]:
            Position.objects.create(
                forum=forum,
                statement_date=statement_date,
                title=title,
                summary=summary,
                source_label=source,
                is_published=True,
            )
    for image_url, alt_text, caption, sort_order in HIGHLIGHTS:
        Highlight.objects.create(
            image_url=image_url,
            alt_text=alt_text,
            caption=caption,
            sort_order=sort_order,
            is_published=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_tag_blogarticle_contributor_blogarticle_ai_assisted_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="GlobalForumPage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("hero_title", models.CharField(default="India at Global Forums", max_length=200)),
                ("hero_subtitle", models.TextField(default="How India takes part in international Internet governance bodies, and the positions shared in those forums.")),
                ("intro_heading", models.CharField(default="Policy topics and organizations", max_length=200)),
                ("intro_text", models.TextField(default="Select a forum to read India’s positions, newest first. Logos and highlight images can be updated from the admin.")),
                ("positions_heading", models.CharField(default="India’s positions", max_length=200)),
                ("highlights_heading", models.CharField(default="Highlights", max_length=200)),
            ],
            options={
                "verbose_name": "Global forums page",
                "verbose_name_plural": "Global forums page",
            },
        ),
        migrations.CreateModel(
            name="GlobalForum",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=80, unique=True)),
                ("tagline", models.CharField(blank=True, max_length=255)),
                ("logo", models.FileField(blank=True, help_text="Upload a logo. A wide mark around 480×160 px works well.", upload_to="global_forums/logos/")),
                ("logo_url", models.URLField(blank=True, help_text="Used when no file is uploaded.", max_length=500)),
                ("logo_style", models.CharField(choices=[("standard", "Standard"), ("wide", "Wide"), ("tall", "Tall")], default="standard", max_length=20)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Global forum",
                "verbose_name_plural": "Global forums",
                "ordering": ("sort_order", "name"),
            },
        ),
        migrations.CreateModel(
            name="GlobalForumHighlight",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.FileField(blank=True, help_text="Upload a photo. 1200×800 px (3:2) fills the frame.", upload_to="global_forums/highlights/")),
                ("image_url", models.URLField(blank=True, help_text="Used when no file is uploaded.", max_length=500)),
                ("alt_text", models.CharField(blank=True, max_length=200)),
                ("caption", models.CharField(blank=True, max_length=400)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Forum highlight",
                "verbose_name_plural": "Forum highlights",
                "ordering": ("sort_order", "id"),
            },
        ),
        migrations.CreateModel(
            name="GlobalForumPosition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("statement_date", models.DateField()),
                ("title", models.CharField(max_length=300)),
                ("summary", models.TextField()),
                ("source_label", models.CharField(blank=True, max_length=200)),
                ("is_published", models.BooleanField(default=True)),
                ("forum", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="positions", to="core.globalforum")),
            ],
            options={
                "verbose_name": "Forum position",
                "verbose_name_plural": "Forum positions",
                "ordering": ("-statement_date", "title"),
            },
        ),
        migrations.RunPython(seed_global_forums, migrations.RunPython.noop),
    ]
