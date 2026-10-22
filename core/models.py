from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ("workshop", "Workshop"),
        ("meeting", "Meeting"),
        ("conference", "Conference"),
    )

    title = models.CharField(max_length=255)
    desc = models.TextField()
    event_datetime = models.DateTimeField()
    type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    join = models.URLField(blank=True, null=True)
    flyer = models.ImageField(upload_to="event_flyers/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    closes_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

class ObserverRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=10)
    organization = models.CharField(max_length=150, blank=True, default='')
    designation = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    reason = models.TextField(blank=True, default='')
    sig = models.CharField(max_length=120)
    work_experience = models.TextField()
    linkedin = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.sig}"

class GroupMaster(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ("code",)

    def __str__(self):
        return f"{self.code} — {self.name}"

class DesignationMaster(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Designation"
        verbose_name_plural = "Designations"
        ordering = ("code",)

    def __str__(self):
        return f"{self.code} — {self.name}"

class SigMember(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)

    group = models.ForeignKey(
        GroupMaster,
        on_delete=models.PROTECT,
        related_name="members"
    )

    designation = models.ForeignKey(
        DesignationMaster,
        on_delete=models.PROTECT,
        related_name="members"
    )

    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Linked Django auth user (created via admin)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SIG(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10, unique=True, help_text="e.g., FI, TPS, DNN")

    def __str__(self):
        return self.name

class SIGProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sigs = models.ManyToManyField(SIG, blank=True, related_name="profiles")
    mobile_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class SIGObserver(models.Model):
    SIG_CHOICES = [
        ("Internet Protocols & Standards", "Internet Protocols & Standards"),
        ("Domain Names & Related Issues", "Domain Names & Related Issues"),
        ("Future of Internet", "Future of Internet"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    sig = models.CharField(max_length=100, choices=SIG_CHOICES)
    work_experience = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.sig}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_users"
    )

    is_dashboard_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class SIGMemberRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    organization = models.CharField(max_length=150)
    designation = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    target_sigs = models.CharField(max_length=255, help_text="Comma separated list of SIGs")
    bio = models.TextField(blank=True)
    linkedin = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.status})"

class Meeting(models.Model):
    MEETING_TYPES = [
        ("FI", "Future of Internet"),
        ("TPS", "Internet Protocols & Standards"),
        ("DNN", "Domain Names & Related Issues"),
        ("Joint", "Joint SIG"),
    ]
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    sig_type = models.CharField(max_length=20, choices=MEETING_TYPES)
    agenda = models.FileField(upload_to="meeting_agendas/", blank=True, null=True)
    minutes = models.FileField(upload_to="meeting_minutes/", blank=True, null=True)
    supporting_document = models.FileField(upload_to="meeting_supporting_docs/", blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.sig_type}"

class MeetingDocument(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="documents")
    document = models.FileField(upload_to="meeting_docs/")
    title = models.CharField(max_length=200)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_admin = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class InternalConsultation(models.Model):
    SIG_TYPES = [
        ("FI", "Future of Internet"),
        ("TPS", "Internet Protocols & Standards"),
        ("DNN", "Domain Names & Related Issues"),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    sig_type = models.CharField(max_length=20, choices=SIG_TYPES)
    brief_document = models.FileField(upload_to="internal_consultations/", blank=True, null=True)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class InternalConsultationResponse(models.Model):
    consultation = models.ForeignKey(
        InternalConsultation, on_delete=models.CASCADE, related_name="responses"
    )
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=150)
    organization = models.CharField(max_length=200)
    response = models.TextField()
    document = models.FileField(upload_to="internal_consultation_responses/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.member.username} - {self.consultation.title}"


class SIGEvent(models.Model):
    """Member-facing SIG schedule events (separate from public `Event` / ig_events admin)."""

    EVENT_TYPE_CHOICES = Event.EVENT_TYPE_CHOICES
    SIG_SCOPE_CHOICES = [
        ("All", "All SIGs"),
        ("FI", "Future of Internet"),
        ("TPS", "Internet Protocols & Standards"),
        ("DNN", "Domain Names & Related Issues"),
        ("Joint", "SIG Joint"),
    ]

    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    event_datetime = models.DateTimeField()
    type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    join = models.URLField(blank=True, null=True)
    sig_scope = models.CharField(max_length=20, choices=SIG_SCOPE_CHOICES, default="All")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("event_datetime",)
        verbose_name = "SIG event"
        verbose_name_plural = "SIG events"

    def __str__(self):
        return self.title


# ---------------------------------------------------------------------------
# Research module — shared broad topics, repository papers, open-source projects
# ---------------------------------------------------------------------------


class ResearchBroadTopic(models.Model):
    """Level 1 — shared by Research Repository and Open Source Projects."""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "Research broad topic"
        verbose_name_plural = "Research broad topics"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:220]
        super().save(*args, **kwargs)


class ResearchSpecificTopic(models.Model):
    """Level 2 — research repository specific topic (e.g. DNS Abuse under Domain Names)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    broad_topic = models.ForeignKey(
        ResearchBroadTopic,
        on_delete=models.CASCADE,
        related_name="specific_research_topics",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    proposed_by_email = models.EmailField(blank=True)
    proposed_by_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("broad_topic", "name")
        unique_together = (("broad_topic", "slug"),)
        verbose_name = "Research specific topic"
        verbose_name_plural = "Research specific topics"

    def __str__(self):
        return f"{self.broad_topic.name} — {self.name}"


class ResearchPaper(models.Model):
    """Level 3 — one version of a paper under a specific topic (versions never overwritten)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    specific_topic = models.ForeignKey(
        ResearchSpecificTopic,
        on_delete=models.CASCADE,
        related_name="papers",
    )
    version = models.PositiveIntegerField(
        editable=False,
        help_text="Auto-assigned: next integer for this specific topic.",
    )
    title = models.CharField(max_length=500)
    abstract = models.TextField(help_text="Short abstract (about 2–3 sentences).")
    document = models.FileField(
        upload_to="research/papers/%Y/%m/",
        help_text="PDF or Word document.",
    )
    is_nixi_intern = models.BooleanField(default=False)
    internship_batch_or_year = models.CharField(max_length=120, blank=True)
    submitter_display_name = models.CharField(max_length=200)
    submitter_email = models.EmailField()
    submitter_account_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ig_account.id when submitted via portal login.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-version", "-uploaded_at")
        verbose_name = "Research paper"
        verbose_name_plural = "Research papers"

    def __str__(self):
        return f"v{self.version} — {self.title[:60]}"

    def clean(self):
        if self.is_nixi_intern and not (self.internship_batch_or_year or "").strip():
            raise ValidationError(
                {"internship_batch_or_year": "Batch or year is required for NIXI interns."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk is None:
            agg = ResearchPaper.objects.filter(
                specific_topic_id=self.specific_topic_id
            ).aggregate(models.Max("version"))
            max_v = agg["version__max"]
            self.version = (max_v or 0) + 1
        super().save(*args, **kwargs)


class OpenSourceProject(models.Model):
    """Level 2 — open source project under a broad topic."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    broad_topic = models.ForeignKey(
        ResearchBroadTopic,
        on_delete=models.CASCADE,
        related_name="open_source_projects",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    proposed_by_email = models.EmailField(blank=True)
    proposed_by_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("broad_topic", "name")
        unique_together = (("broad_topic", "slug"),)
        verbose_name = "Open source project"
        verbose_name_plural = "Open source projects"

    def __str__(self):
        return self.name


class OpenSourceContribution(models.Model):
    """Level 3 — contribution / version to a project (files or URL; versions cumulative)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    project = models.ForeignKey(
        OpenSourceProject,
        on_delete=models.CASCADE,
        related_name="contributions",
    )
    version = models.PositiveIntegerField(
        editable=False,
        help_text="Auto-assigned per project.",
    )
    title = models.CharField(max_length=300, help_text="Short title for this contribution.")
    summary = models.TextField(blank=True)
    contribution_file = models.FileField(
        upload_to="research/oss/%Y/%m/",
        blank=True,
        null=True,
        help_text="Optional file (PDF, Word, etc.).",
    )
    external_url = models.URLField(blank=True, max_length=500)
    contributor_display_name = models.CharField(max_length=200)
    contributor_email = models.EmailField()
    contributor_account_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-version", "-uploaded_at")
        verbose_name = "Open source contribution"
        verbose_name_plural = "Open source contributions"

    def __str__(self):
        return f"v{self.version} — {self.title[:50]}"

    def clean(self):
        if not self.contribution_file and not (self.external_url or "").strip():
            raise ValidationError(
                "Provide a file upload or an external URL."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk is None:
            agg = OpenSourceContribution.objects.filter(
                project_id=self.project_id
            ).aggregate(models.Max("version"))
            max_v = agg["version__max"]
            self.version = (max_v or 0) + 1
        super().save(*args, **kwargs)



from django.db import models

class BlogArticle(models.Model):

        STATUS_CHOICES = (
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
        )

        title = models.CharField(max_length=255)

        member_uuid = models.CharField(max_length=255)

        article_type = models.CharField(max_length=100)
        read_time = models.CharField(max_length=50, blank=True, null=True)

        Contributor = models.CharField(
            max_length=100,
            blank=True,
            null=True
        )

        tags = models.CharField(
            max_length=255,
            blank=True,
            null=True
        )

        custom_tags = models.CharField(
            max_length=500,
            blank=True,
            null=True
        )

        ai_assisted = models.CharField(
            max_length=20,
            blank=True,
            null=True
        )

        previously_published = models.CharField(
            max_length=10,
            blank=True,
            null=True
        )

        image = models.ImageField(
            upload_to='blog_articles/',
            blank=True,
            null=True,
            help_text="Upload a cover at 1600 × 900 px (16:9), JPG or PNG. Blog cards and the article page use this shape.",
        )

        article_file = models.FileField(
            upload_to='blog_articles/files/',
            blank=True,
            null=True
        )

        description = models.TextField()

        content = models.TextField(
            blank=True,
            null=True
        )

        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='Pending'
        )

        created_at = models.DateTimeField(
            auto_now_add=True
        )
        total_read_seconds = models.PositiveIntegerField(
            default=0
        )

        total_views = models.PositiveIntegerField(
            default=0
        )

        def __str__(self):
            return self.title



class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GlobalForumPage(models.Model):
    """Editable copy for the India at Global Forums page. One row is used."""

    hero_title = models.CharField(max_length=200, default="India at Global Forums")
    hero_subtitle = models.TextField(
        default="How India takes part in international Internet governance bodies, and the positions shared in those forums."
    )
    intro_heading = models.CharField(max_length=200, default="Policy topics and organizations")
    intro_text = models.TextField(
        default="Select a forum to read India’s positions, newest first. Logos and highlight images can be updated from the admin."
    )
    positions_heading = models.CharField(max_length=200, default="India’s positions")
    highlights_heading = models.CharField(max_length=200, default="Highlights")

    class Meta:
        verbose_name = "Global forums page"
        verbose_name_plural = "Global forums page"

    def __str__(self):
        return self.hero_title


class GlobalForum(models.Model):
    """A forum tile on the India at Global Forums page."""

    class LogoStyle(models.TextChoices):
        STANDARD = "standard", "Standard"
        WIDE = "wide", "Wide"
        TALL = "tall", "Tall"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=80, unique=True)
    tagline = models.CharField(max_length=255, blank=True)
    logo = models.FileField(
        upload_to="global_forums/logos/",
        blank=True,
        help_text="Upload a logo at 480 × 160 px, PNG with a transparent background. It is shown inside a small tile, so a wide mark stays readable.",
    )
    logo_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Used when no file is uploaded.",
    )
    logo_style = models.CharField(
        max_length=20,
        choices=LogoStyle.choices,
        default=LogoStyle.STANDARD,
    )
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "Global forum"
        verbose_name_plural = "Global forums"

    def __str__(self):
        return self.name

    @property
    def picture_url(self):
        if self.logo:
            return self.logo.url
        return self.logo_url or ""


class GlobalForumPosition(models.Model):
    """A dated statement shown when a forum is selected."""

    forum = models.ForeignKey(
        GlobalForum,
        on_delete=models.CASCADE,
        related_name="positions",
    )
    statement_date = models.DateField()
    title = models.CharField(max_length=300)
    summary = models.TextField()
    source_label = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("-statement_date", "title")
        verbose_name = "Forum position"
        verbose_name_plural = "Forum positions"

    def __str__(self):
        return self.title


class GlobalForumHighlight(models.Model):
    """A slide in the highlights carousel."""

    image = models.FileField(
        upload_to="global_forums/highlights/",
        blank=True,
        help_text="Upload a photo at 1500 × 500 px (3:1), JPG or PNG. That size fills the highlights strip on large screens and stays sharp on phones.",
    )
    image_url = models.URLField(
        blank=True,
        max_length=500,
        help_text="Used when no file is uploaded.",
    )
    alt_text = models.CharField(max_length=200, blank=True)
    caption = models.CharField(max_length=400, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "Forum highlight"
        verbose_name_plural = "Forum highlights"

    def __str__(self):
        return self.caption or self.alt_text or f"Highlight {self.pk}"

    @property
    def picture_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ""